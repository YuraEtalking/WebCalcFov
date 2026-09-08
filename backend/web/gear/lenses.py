from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.crud.lens import (
    get_active_lenses,
    get_active_lens_with_teleconverters
)
from backend.services.detail_pages_service import images_by_role
from backend.services.compare_service import get_ids
from backend.web.templates import render
from backend.web.constants import COMPARE_LENSES_COOKIE

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
        'gear/lens_list.html',
        lenses=lenses,
        slug=slug,
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
    images = images_by_role(entity=lens, role='photo')
    mtfs = images_by_role(entity=lens, role='mtf')
    sample_photos = images_by_role(entity=lens, role='sample')

    # raw = request.cookies.get('compare_lenses', '')
    # compare_ids = [int(x) for x in raw.split(',') if x.isdigit()]

    compare_ids = get_ids(request, COMPARE_LENSES_COOKIE)
    logger.debug('compare_ids: compare_ids="{}"', compare_ids)

    return render(
            request,
            'gear/lens_detail.html',
            lens=lens,
            slug=slug,
            images=images,
            mtfs=mtfs,
            sample_photos=sample_photos,
            compare_ids=compare_ids,
        )