from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, union
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.models import Camera, Lens
from backend.web.templates import render


web_router = APIRouter(
    prefix='/wiki',
    tags=['Wiki'],)
templates = Jinja2Templates(directory='templates')


@web_router.get('/', name='wiki', response_class=HTMLResponse)
async def wiki(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    camera_manufacturers = select(Camera.manufacturer.label('manufacturer'))
    lens_manufacturers = select(Lens.manufacturer.label('manufacturer'))

    stmt = (
        union(camera_manufacturers, lens_manufacturers)
        .order_by('manufacturer')
    )

    result = await session.scalars(stmt)
    manufacturers = result.all()

    return render(request, 'wiki.html', {'manufacturers': manufacturers})



@web_router.get(
    '/{slug}',
    name='manufacturer',
    response_class=HTMLResponse
)
async def manufacturer(request: Request, slug: str):
    return render(
        request,
        'manufacturer.html',
        {'slug': slug}
    )
