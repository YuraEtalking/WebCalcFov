from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Camera


async def get_active_cameras(session: AsyncSession, manufacturer=None):
    """Получаем список активных камер, всех или по производителю."""
    stmt = select(Camera).where(Camera.is_active.is_(True))

    if manufacturer is not None:
        stmt = stmt.where(Camera.manufacturer == manufacturer)

    result = await session.execute(stmt)
    active_cameras = result.scalars().all()
    return active_cameras


async def get_active_camera_with_sensor(camera_id, session: AsyncSession):
    """Получаем камеру и сенсор этой камеры."""
    stmt = await session.execute(select(
        Camera
    ).options(
        joinedload(Camera.sensor),
        selectinload(Camera.camera_lenses),
        selectinload(Camera.compatible_lenses),
    ).where(
        Camera.id == camera_id,
        Camera.is_active.is_(True),
    ))
    camera = stmt.scalars().first()
    return camera
