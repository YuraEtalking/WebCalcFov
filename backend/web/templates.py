from urllib.parse import urlencode

from fastapi import Request
from fastapi.templating import Jinja2Templates


from backend.web.i18n import SUPPORTED_LANGUAGES

templates = Jinja2Templates(directory='templates')


def render(request: Request, template_name: str, context: dict | None = None):
    base_context = {
        'request': request,
        '_': request.state._,
        'lang': request.state.lang,
        'language_url': lambda lang: language_url(request, lang),
    }
    if context is not None:
        base_context.update(context)

    response = templates.TemplateResponse(template_name, base_context)

    query_lang = request.query_params.get('lang')
    if query_lang in SUPPORTED_LANGUAGES:
        response.set_cookie(
            key='lang',
            value=query_lang,
            max_age=60 * 60 * 24 * 365,
            samesite='lax',
        )

    return response


def language_url(request: Request, lang: str) -> str:
    if lang not in SUPPORTED_LANGUAGES:
        lang = request.state.lang

    query_params = dict(request.query_params)
    query_params['lang'] = lang

    return f'{request.url.path}?{urlencode(query_params)}'
