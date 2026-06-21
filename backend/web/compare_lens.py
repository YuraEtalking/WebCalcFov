from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.core.db import get_async_session
from backend.web.templates import render
from backend.crud.lens import get_lenses_for_compare


compare_router = APIRouter(
    # prefix='/compare',
    # tags=['Compare'],
)

@compare_router.post(
    '/compare/lenses/add/{lens_id}',
    name='add_lens_compare',
    # response_class=HTMLResponse,
)
async def add_lend_to_compare(request: Request, lens_id: int):

    raw = request.cookies.get('compare_lenses', '')
    ids = [int(x) for x in raw.split(',') if x.isdigit()]

    if lens_id not in ids:
        ids.append(lens_id)

    ids = ids[:4]
    response = Response(status_code=204)
    response.set_cookie(
        key='compare_lenses',
        value=','.join(map(str, ids)),
        max_age=60 * 60 * 24 * 30,
        samesite='lax',
    )
    return response


@compare_router.get('/compare/lenses', name='lens_compare',)
async def compare_lenses(request: Request, session: AsyncSession = Depends(get_async_session)):
    raw = request.cookies.get('compare_lenses', '')
    ids = [int(x) for x in raw.split(',') if x.isdigit()]

    logger.debug('Было: ids="{}"', ids)

    lenses = await get_lenses_for_compare(ids, session)
    return render(request, 'wiki/compare_lens.html', {
        'lenses': lenses,
    })


@compare_router.post(
    '/compare/lenses/remove/{lens_id}',
    name='remove_lens_comparison_list',
    # response_class=HTMLResponse,
)
async def remove_from_comparison_list(request: Request, lens_id: int):

    raw = request.cookies.get('compare_lenses', '')
    ids = [int(x) for x in raw.split(',') if x.isdigit()]

    if lens_id in ids:
        ids.remove(lens_id)

    logger.debug('Стало: ids="{}"', ids)
    response = Response(status_code=204)
    response.set_cookie(
        key='compare_lenses',
        value=','.join(map(str, ids)),
        max_age=60 * 60 * 24 * 30,
        samesite='lax',
    )
    return response


@compare_router.post(
    '/compare/lenses/clear/',
    name='clear_comparison_list',
    # response_class=HTMLResponse,
)
async def clear_comparison_list(request: Request):

    raw = request.cookies.get('compare_lenses', '')
    ids = [int(x) for x in raw.split(',') if x.isdigit()]

    ids.clear()

    logger.debug('Стало: ids="{}"', ids)
    response = Response(status_code=204)
    response.set_cookie(
        key='compare_lenses',
        value=','.join(map(str, ids)),
        max_age=60 * 60 * 24 * 30,
        samesite='lax',
    )
    return response