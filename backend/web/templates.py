from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')


def render(request: Request, template_name: str, context: dict):
    base_context = {
        'request': request,
        '_': request.state._,
        'lang': request.state.lang,
    }

    base_context.update(context)

    return templates.TemplateResponse(template_name, base_context)