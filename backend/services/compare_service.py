from http import HTTPStatus

from fastapi import Request
from fastapi.responses import Response, RedirectResponse
from loguru import logger

from backend.web.templates import set_default_cookie


def parse_ids(raw: str | None) -> list[int]:
    """Переводим строку id из куки в список."""
    if not raw:
        return []
    logger.debug('raw: raw="{}"', raw)
    return [int(x) for x in raw.split(',') if x.isdigit()]


def get_ids(request: Request, key: str) -> list[int]:
    """Отдает подготовленный список id."""
    return parse_ids(request.cookies.get(key))


def serialize_ids_for_cookie(ids: list[int]):
    """Переводим список c id в строку для куки."""
    return ','.join(map(str, ids))


def add_to_compare(request: Request, obj_id: int, compare_list: str):
    """Добавляет id объекта в список сравнений."""
    ids = get_ids(request, compare_list)
    if obj_id not in ids:
        ids.append(obj_id)

    ids = ids[:4]
    logger.debug('Куки после добавления в compare_list="{}": obj_id="{}", ids="{}"',compare_list, obj_id, ids)
    response = RedirectResponse(
        url=request.headers.get('referer'),
        status_code=HTTPStatus.SEE_OTHER
    )
    set_default_cookie(
        response=response,
        key=compare_list,
        value=serialize_ids_for_cookie(ids)
    )
    return response


def remove_from_comparison_list(
        request: Request,
        obj_id: int,
        compare_list: str,
):
    """Удаляет id объекта из списка сравнений."""
    ids = get_ids(request, compare_list)
    if obj_id in ids:
        ids.remove(obj_id)

    logger.debug('Куки после удаления объектива: ids="{}"', ids)
    response = RedirectResponse(
        url=request.headers.get('referer'),
        status_code=HTTPStatus.SEE_OTHER
    )
    set_default_cookie(
        response=response,
        key=compare_list,
        value=serialize_ids_for_cookie(ids)
    )
    return response

def clear_list_of_comparison(request: Request, compare_list: str):
    """Чистит список сравнений."""
    response = RedirectResponse(
        url=request.headers.get('referer'),
        status_code=HTTPStatus.SEE_OTHER
    )
    response.delete_cookie(
        key=compare_list,
        samesite='lax',
    )
    ids = get_ids(request, compare_list)
    logger.debug('Очистили список куки объектива: ids="{}"', ids)
    return response