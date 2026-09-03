from http import HTTPStatus

from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.core.db import get_async_session
from backend.web.templates import render
from backend.crud.lens import get_lenses_for_compare
from backend.services.compare_service import (
    get_ids,
    add_to_compare,
    remove_from_comparison_list,
    clear_list_of_comparison,
)
from backend.web.constants import COMPARE_LENSES_COOKIE



web_router = APIRouter(
    tags=['Compare'],
)


@web_router.post('/lenses/add/{lens_id}', name='add_lens_compare')
async def add_lens_to_compare(request: Request, lens_id: int):
    """Добавляет линзу в список сравнений."""
    return add_to_compare(
        request=request,
        obj_id=lens_id,
        compare_list=COMPARE_LENSES_COOKIE,
    )


@web_router.get('/lenses', name='lens_compare',)
async def compare_lenses(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """Представление сравнений объективов."""
    ids = get_ids(request, COMPARE_LENSES_COOKIE)

    lenses = await get_lenses_for_compare(ids, session)
    return render(
        request,
        'gear/compare/lens_comparison.html',
        {
            'lenses': lenses,
        }
    )


@web_router.post(
    '/lenses/remove/{lens_id}',
    name='remove_lens_comparison_list',
)
async def remove_lens_from_comparison_list(request: Request, lens_id: int):
    """Удаляет объектив из списка сравнений."""
    return remove_from_comparison_list(
        request=request,
        obj_id=lens_id,
        compare_list=COMPARE_LENSES_COOKIE,
    )


@web_router.post('/lenses/clear/',name='clear_comparison_list')
async def clear_list_of_lenses_for_comparison(request: Request):
    """Чистит список сравнений объективов."""
    return clear_list_of_comparison(request, COMPARE_LENSES_COOKIE)