from sqlalchemy import select, union
from sqlalchemy.orm import joinedload, with_loader_criteria
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Lens, CameraLens, LensImageLink, Image, Camera, Teleconverter

async def get_manufacturers(session: AsyncSession):
    camera_manufacturers = select(Camera.manufacturer.label('manufacturer'))
    lens_manufacturers = select(Lens.manufacturer.label('manufacturer'))

    stmt = (
        union(camera_manufacturers, lens_manufacturers)
        .order_by('manufacturer')
    )

    result = await session.scalars(stmt)
    return result.all()