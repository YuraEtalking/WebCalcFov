import gettext

from fastapi import Request
from loguru import logger

SUPPORTED_LANGUAGES = ['ru', 'en']
DEFAULT_LANGUAGE = 'ru'

LOCALES_DIR = 'locales'
DOMAIN = 'messages'


def get_locale(request: Request) -> str:
    """
    Определяем язык пользователя.
    Приоритет:
    1. query-параметр ?lang=ru
    2. cookie lang
    3. язык по умолчанию
    """

    lang = request.query_params.get('lang')

    if lang in SUPPORTED_LANGUAGES:
        return lang

    lang = request.cookies.get('lang')
    logger.debug('lang="{}"', lang)

    if lang in SUPPORTED_LANGUAGES:
        return lang

    return DEFAULT_LANGUAGE


def get_translation(lang: str):
    try:
        return gettext.translation(
            DOMAIN,
            localedir=LOCALES_DIR,
            languages=[lang],
        )
    except FileNotFoundError:
        return gettext.NullTranslations()


async def i18n_middleware(request: Request, call_next):
    lang = get_locale(request)
    translation = get_translation(lang)

    request.state.lang = lang
    request.state._ = translation.gettext

    response = await call_next(request)
    return response