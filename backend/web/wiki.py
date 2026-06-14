from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from sqlalchemy import select, union
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.crud.manufacturers import get_manufacturers
from backend.models import Camera, Lens
from backend.web.templates import render


web_router = APIRouter(tags=['Wiki'])


@web_router.get('/', name='wiki', response_class=HTMLResponse)
async def wiki(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    manufacturers = await get_manufacturers(session)
    return render(
        request,
        'wiki/manufacturer_list.html',
        {'manufacturers': manufacturers}
    )



@web_router.get(
    '/{slug}',
    name='manufacturer',
    response_class=HTMLResponse
)
async def manufacturer(request: Request, slug: str):
    return render(
        request,
        'wiki/manufacturer.html',
        {'slug': slug}
    )
