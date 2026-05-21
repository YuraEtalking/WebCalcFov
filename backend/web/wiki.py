from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

web_router = APIRouter(
    prefix='/wiki',
    tags=['Wiki'],)
templates = Jinja2Templates(directory='templates')


@web_router.get('/', name='wiki', response_class=HTMLResponse)
async def wiki(request: Request):
    return templates.TemplateResponse('wiki.html', {'request': request})
