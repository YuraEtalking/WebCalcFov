from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from loguru import logger

from backend.core.db import get_async_session
from backend.web.templates import render
from backend.models import Camera
from backend.services.exposure_equivalence import (
    CameraInput,
    ExposureInputError,
    ExposureSettings,
    calculate,
    parse_shutter,
)

web_router = APIRouter(tags=['tools'])

TEMPLATE = 'tools/exposure_equivalence.html'

# Префиксы полей формы. Обязательны эталон и первая сравниваемая камера.
SLOT_REFERENCE = 'reference'
SLOT_TARGETS = ('target_1', 'target_2')
FORM_FIELDS = ('camera_id', 'focal_length_mm', 'aperture', 'shutter', 'iso')


async def _load_cameras(session: AsyncSession) -> list[Camera]:
    stmt = (
        select(Camera)
        .options(selectinload(Camera.spec))
        .where(Camera.is_active.is_(True))
        .order_by(Camera.name)
    )
    return list((await session.scalars(stmt)).all())


def _crop_factor(camera: Camera) -> float | None:
    """Camera.spec и размеры сенсора могут быть None — тогда None."""
    return camera.spec.crop_factor if camera.spec is not None else None


def _to_float(raw: str, label: str) -> float:
    try:
        return float(raw.replace(',', '.'))
    except (ValueError, AttributeError) as exc:
        raise ExposureInputError(f'{label} must be a number.') from exc


def _raw_slot(form, prefix: str) -> dict[str, str]:
    """Сырые строки из формы для повторного заполнения полей."""
    return {name: (form.get(f'{prefix}_{name}') or '').strip() for name in FORM_FIELDS}


def _build_camera_input(
    raw: dict[str, str],
    cameras_by_id: dict[int, Camera],
    label: str,
) -> CameraInput:
    try:
        camera_id = int(raw['camera_id'])
    except ValueError as exc:
        raise ExposureInputError(f'{label}: select a camera.') from exc

    camera = cameras_by_id.get(camera_id)
    if camera is None:
        raise ExposureInputError(f'{label}: camera not found.')

    try:
        settings = ExposureSettings(
            focal_length_mm=_to_float(raw['focal_length_mm'], 'Focal length'),
            aperture=_to_float(raw['aperture'], 'Aperture'),
            shutter_seconds=parse_shutter(raw['shutter']),
            iso=_to_float(raw['iso'], 'ISO'),
        )
    except ExposureInputError as exc:
        raise ExposureInputError(f'{label}: {exc}') from exc

    return CameraInput(
        camera_id=camera.id,
        camera_name=camera.name,
        crop_factor=_crop_factor(camera),
        settings=settings,
    )


def _render(request: Request, cameras: list[Camera], **context):
    return render(request, TEMPLATE, {'cameras': cameras, **context})


@web_router.get(
    '/exposure_equivalence',
    name='exposure_equivalence',
    response_class=HTMLResponse,
)
async def exposure_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    cameras = await _load_cameras(session)
    return _render(request, cameras, data=None, result=None)



@web_router.post(
    '/exposure_equivalence',
    name='exposure_submit',
    response_class=HTMLResponse,
)
async def exposure_submit(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    form = await request.form()
    cameras = await _load_cameras(session)
    cameras_by_id = {camera.id: camera for camera in cameras}

    # Сырые значения всегда возвращаем в шаблон, чтобы форма не очищалась.
    data = {SLOT_REFERENCE: _raw_slot(form, SLOT_REFERENCE)}
    logger.debug('data: data="{}"', data)
    for slot in SLOT_TARGETS:
        data[slot] = _raw_slot(form, slot)
    logger.debug('data: data="{}"', data)
    try:
        reference = _build_camera_input(
            data[SLOT_REFERENCE], cameras_by_id, 'Reference camera',
        )
        targets: list[CameraInput] = []
        for index, slot in enumerate(SLOT_TARGETS, start=1):
            raw = data[slot]
            # Вторая сравниваемая камера необязательна: пустой select — пропускаем.
            if not raw['camera_id'] and index > 1:
                continue
            targets.append(_build_camera_input(raw, cameras_by_id, f'Camera {index}'))

        result = calculate(reference, targets)
    except ExposureInputError as exc:
        return _render(
            request, cameras,
            data=data, result=None,
            message=str(exc), message_type='error',
        )

    return _render(request, cameras, data=data, result=result)