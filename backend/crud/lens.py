from sqlalchemy import select
from sqlalchemy.orm import joinedload, with_loader_criteria
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Lens, CameraLens, LensImageLink, Image, Camera, Teleconverter


async def get_active_lenses(session: AsyncSession, manufacturer=None):
    """Получаем список активных объективов."""
    stmt = select(
        Lens
    ).where(Lens.is_active.is_(True)).order_by(Lens.focal_tele)

    if manufacturer is not None:
        stmt = stmt.where(Lens.manufacturer == manufacturer)

    result = await session.execute(stmt)
    active_lenses = result.scalars().all()
    return active_lenses


async def get_active_lens_with_teleconverters(lens_id, session: AsyncSession):
    """Получаем объектив и подходящие телеконверторы."""
    stmt = await session.execute(select(
        Lens
    ).options(
        joinedload(Lens.teleconverters),
        joinedload(Lens.links),
        joinedload(Lens.compatible_cameras),
        joinedload(Lens.camera_lenses).joinedload(CameraLens.camera),
        joinedload(Lens.spec),
        joinedload(Lens.image_links).joinedload(LensImageLink.image),

        with_loader_criteria(Image, Image.is_active.is_(True)),
        with_loader_criteria(Camera, Camera.is_active.is_(True)),
        with_loader_criteria(Teleconverter, Teleconverter.is_active.is_(True)),
    ).where(
        Lens.id == lens_id,
        Lens.is_active.is_(True)
    ))
    lens = stmt.scalars().unique().first()
    return lens


async def get_lenses_for_compare(ids: list[int], session: AsyncSession):
    """Получаем объектив и подходящие телеконверторы."""
    stmt = await session.execute(select(
        Lens
    ).options(
        joinedload(Lens.teleconverters),
        joinedload(Lens.compatible_cameras),
        joinedload(Lens.camera_lenses).joinedload(CameraLens.camera),
        joinedload(Lens.spec),
        joinedload(Lens.image_links).joinedload(LensImageLink.image),

        with_loader_criteria(Image, Image.is_active.is_(True)),
        with_loader_criteria(Camera, Camera.is_active.is_(True)),
        with_loader_criteria(Teleconverter, Teleconverter.is_active.is_(True)),
    ).where(
        Lens.id.in_(ids),
        Lens.is_active.is_(True)
    ))
    lenses = list(stmt.scalars().unique())
    return lenses
