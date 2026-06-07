from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.crud.lens import get_active_lenses, get_active_lens_with_teleconverters
from backend.web.templates import render


web_router = APIRouter(
    prefix='/lenses',
    tags=['Lenses'],
)

@web_router.get('/', name='lens_list', response_class=HTMLResponse)
async def lens_list(
        request: Request,
        slug: str,
        session: AsyncSession = Depends(get_async_session)
):
    lenses = await get_active_lenses(session, slug)
    return render(
        request,
        'wiki/lens_list.html',
        {'lenses': lenses, 'slug': slug,}
    )



@web_router.get(
    '/{lens_id}',
    name='lens_detail',
    response_class=HTMLResponse,
)
async def lens_detail(
        request: Request,
        lens_id: int,
        slug: str,
        session: AsyncSession = Depends(get_async_session)
):
    lens = await get_active_lens_with_teleconverters(lens_id, session)
    logger.debug('lens.camera_lenses="{}"', lens.camera_lenses)

    return render(
            request,
            'wiki/lens_detail.html',
            {
                'lens':  lens,
                'slug':slug,
                'links': lens.links,
                'teleconverters': lens.teleconverters,
                'compatible_cameras': lens.compatible_cameras,
                'camera_lenses': lens.camera_lenses,
                'spec': lens.spec,
            }
        )