from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Lens, Teleconverter


async def get_active_lenses(session: AsyncSession):
    """Получаем список активных объективов."""
    stmt = await session.execute(select(
        Lens
    ).where(Lens.is_active.is_(True)).order_by(Lens.focal_max))
    active_lenses = stmt.scalars().all()
    return active_lenses


async def get_active_lens_with_teleconverters(lens_id, session: AsyncSession):
    """Получаем объектив и подходящие телеконверторы."""
    stmt = await session.execute(select(
        Lens
    ).options(
        joinedload(Lens.teleconverters)
    ).where(
        Lens.id == lens_id,
        Lens.is_active.is_(True)
    ))
    lens = stmt.scalars().first()
    return lens
