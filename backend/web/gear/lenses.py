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
        'gear/lens_list.html',
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
    images = [
        link.image for link in lens.image_links if link.role == 'photo' and link.image is not None
    ]
    mtfs = [link.image for link in lens.image_links if link.role == 'mtf' and link.image is not None]
    sample_photos = [link.image for link in lens.image_links if link.role == 'sample' and link.image is not None]
    raw = request.cookies.get('compare_lenses', '')
    compare_ids = [int(x) for x in raw.split(',') if x.isdigit()]
    return render(
            request,
            'gear/lens_detail.html',
            {
                'lens':  lens,
                'slug':slug,
                'links': lens.links,
                'teleconverters': lens.teleconverters,
                'compatible_cameras': lens.compatible_cameras,
                'camera_lenses': lens.camera_lenses,
                'spec': lens.spec,
                'images': images,
                'mtfs': mtfs,
                'sample_photos': sample_photos,
                'compare_ids': compare_ids,
            }
        )