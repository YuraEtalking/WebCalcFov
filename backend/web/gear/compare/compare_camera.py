from http import HTTPStatus

from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.core.db import get_async_session
from backend.web.templates import render
from backend.crud.lens import get_lenses_for_compare
from backend.services.compare_service import get_ids
from backend.web.templates import set_default_cookie
from backend.web.constants import COMPARE_CAMERAS_COOKIE



web_router = APIRouter(
    tags=['Compare'],
)

def serialize_ids_for_cookie(ids: list[int]):
    return ','.join(map(str, ids))


@web_router.post(
    '/camera/add/{camera_id}',
    name='add_camera_to_compare',
)
async def add_camera_to_compare(request: Request, camera_id: int):
    """."""
    ids = get_ids(request, COMPARE_CAMERAS_COOKIE)

    if camera_id not in ids:
        ids.append(camera_id)

    ids = ids[:4]

    response = RedirectResponse(
        url=request.headers.get('referer'),
        status_code=HTTPStatus.SEE_OTHER
    )
    set_default_cookie(
        response=response,
        key=COMPARE_CAMERAS_COOKIE,
        value=serialize_ids_for_cookie(ids)
    )
    return response


# @web_router.get('/lenses', name='lens_compare',)
# async def compare_lenses(
#         request: Request,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     """Представление сравнений объективов."""
#     ids = get_ids(request, COMPARE_LENSES_COOKIE)
#     logger.debug('Было: ids="{}"', ids)
#
#     lenses = await get_lenses_for_compare(ids, session)
#     return render(request, 'gear/compare/lens_comparison.html', {
#         'lenses': lenses,
#     })
#
#
# @web_router.post(
#     '/lenses/remove/{lens_id}',
#     name='remove_lens_comparison_list',
# )
# async def remove_from_comparison_list(request: Request, lens_id: int):
#     """Удаляет объектив из списка сравнений."""
#     ids = get_ids(request, COMPARE_LENSES_COOKIE)
#     if lens_id in ids:
#         ids.remove(lens_id)
#
#     logger.debug('Стало: ids="{}"', ids)
#     response = RedirectResponse(
#         url=request.headers.get('referer'),
#         status_code=HTTPStatus.SEE_OTHER
#     )
#     set_default_cookie(
#         response=response,
#         key=COMPARE_LENSES_COOKIE,
#         value=serialize_ids_for_cookie(ids)
#     )
#     return response
#
#
# @web_router.post(
#     '/lenses/clear/',
#     name='clear_comparison_list',
# )
# async def clear_comparison_list(request: Request):
#     """Чистит список сравнений."""
#     response = RedirectResponse(
#         url=request.headers.get('referer'),
#         status_code=HTTPStatus.SEE_OTHER
#     )
#     response.delete_cookie(
#         key=COMPARE_LENSES_COOKIE,
#         samesite='lax',
#     )
#     return response