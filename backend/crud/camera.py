from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from backend.models import Camera


async def get_active_cameras(session: AsyncSession):
    """Получаем список активных камер."""
    stmt = await session.execute(select(
        Camera
    ).where(Camera.is_active.is_(True)))
    active_cameras = stmt.scalars().all()
    return active_cameras


async def get_camera_with_sensor(camera_id, session: AsyncSession):
    """Получаем камеру и сенсор этой камеры."""
    stmt = await session.execute(select(
        Camera
    ).options(
        joinedload(Camera.sensor)
    ).where(Camera.id == camera_id))
    camera = stmt.scalars().first()
    return camera
