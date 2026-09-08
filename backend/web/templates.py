from urllib.parse import urlencode
from typing import Any

from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from loguru import logger

from backend.web.i18n import SUPPORTED_LANGUAGES
from backend.web.constants import MAX_AGE_30_DAYS, LANG

templates = Jinja2Templates(directory='templates')


def set_default_cookie(
        response: Response,
        key: str,
        value: Any,
        max_age: int = MAX_AGE_30_DAYS,
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        samesite='lax',
        # httponly=True
        # secure=True,    # в прод при HTTPS
    )


def render(request: Request, template_name: str, **context: Any):
    """Рендерит шаблон с сохранением выбранного языка."""
    base_context = {
        'request': request,
        '_': request.state._,
        LANG: request.state.lang,
        'language_url': lambda lang: language_url(request, lang),
    }
    if context is not None:
        base_context.update(context)

    response = templates.TemplateResponse(template_name, base_context)

    query_lang = request.query_params.get(LANG)
    if query_lang in SUPPORTED_LANGUAGES:
        set_default_cookie(response=response, key=LANG, value=query_lang)

    return response


def language_url(request: Request, lang: str) -> str:
    if lang not in SUPPORTED_LANGUAGES:
        lang = request.state.lang

    query_params = dict(request.query_params)
    query_params[LANG] = lang

    return f'{request.url.path}?{urlencode(query_params)}'
