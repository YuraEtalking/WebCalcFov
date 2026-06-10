from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from backend.core.constants.message_constants import (
    WARNING_CAMERA_AND_LENS_INCOMPATIBILITY
)
from backend.crud.camera import get_active_camera_with_sensor
from backend.crud.lens import get_active_lens_with_teleconverters
from backend.schemas.fov import FovCalcInput
from backend.services.fov_calculator import calculate_fov

from backend.models.teleconverter import Teleconverter
from backend.models.associative_model import CameraLens


class FovServiceError(Exception):
    pass


class EntityNotFoundError(FovServiceError):
    pass


class InvalidFovInputError(FovServiceError):
    pass


def get_list_teleconverters(
        lens_teleconverters: list[Teleconverter]
) -> list[dict]:
    """Отдает список словарей телеконверторов с уникальным multiplier"""
    tc_list = []
    if lens_teleconverters:
        for tc in lens_teleconverters:
            if not any(tc.multiplier == i['multiplier'] for i in tc_list):
                tc_list.append({
                    'multiplier': tc.multiplier,
                    'teleconverter_id': tc.id,
                })

    return tc_list


def check_camera_and_lens_compatibility(
        lens_id: int,
        camera_lenses: list[CameraLens],
) -> bool:
    """Проверяет совместимость камеры и объектива."""
    return any(cl.lens_id == lens_id for cl in camera_lenses)


def checking_distance_within_range(
        focal: float,
        focal_wide: int,
        focal_tele: int,
) -> float:
    """Проверка focal не None и не выходит за диапазон фокусных."""
    if focal is None:
        focal = focal_tele

    if not focal_wide <= focal <= focal_tele:
        raise InvalidFovInputError('Фокусное выходит за диапазон объектива')

    return focal



async def prepare_fov_response_data(
        input_data: FovCalcInput,
        session: AsyncSession
) -> dict[str, Any]:
    """Подготавливает данные для ответа."""
    lens = await get_active_lens_with_teleconverters(
        input_data.lens_id,
        session,
    )
    if not lens:
        raise EntityNotFoundError('Объектив не выбран')

    camera = await get_active_camera_with_sensor(input_data.camera_id, session)
    if not camera:
        raise EntityNotFoundError('Камера не выбрана')

    message = 'Расчёт выполнен'
    message_type = 'success'

    if not check_camera_and_lens_compatibility(
            lens_id=input_data.lens_id,
            camera_lenses=camera.camera_lenses,
    ):
        message = WARNING_CAMERA_AND_LENS_INCOMPATIBILITY
        message_type = 'warning'

    selected_tc = None
    if input_data.teleconverter_id is not None:
        selected_tc_obj = next(
            (
                tc for tc in lens.teleconverters
                if tc.id == input_data.teleconverter_id
            ),
            None
        )
        if selected_tc_obj is None:
            raise FovServiceError(
                'Выбранный телеконвертер не принадлежит объективу'
            )
        selected_tc = selected_tc_obj.multiplier

    focal = checking_distance_within_range(
        focal=input_data.focal,
        focal_wide=lens.focal_wide,
        focal_tele=lens.focal_tele,
    )

    result = calculate_fov(
        sensor=camera.sensor,
        focal=focal,
        distance=input_data.distance,
        selected_tc=selected_tc
    )
    teleconverters = get_list_teleconverters(lens.teleconverters)
    return {
        'data': {
            'camera': camera,
            'lens': lens,
            'sensor': camera.sensor,
            'distance': input_data.distance,
            'lens_list': camera.compatible_lenses,
        },
        'result': result,
        'focal': focal,
        'teleconverter_id': input_data.teleconverter_id,
        'teleconverters': teleconverters,
        'message': message,
        'message_type': message_type,
    }


async def get_lens_data(lens_id: int, session: AsyncSession) -> dict[str, Any]:
    lens = await get_active_lens_with_teleconverters(lens_id, session)

    if not lens:
        raise EntityNotFoundError('Объектив не выбран')

    teleconverters = get_list_teleconverters(lens.teleconverters)

    return {
            'lens': lens,
            'focal': lens.focal_tele,
            'teleconverters': teleconverters,
    }
