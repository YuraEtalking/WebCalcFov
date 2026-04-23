from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError


web_router = APIRouter()

web_router.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static',
)
templates = Jinja2Templates(directory='templates')

@web_router.get('/', response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse('form.html', {
        'request': request,
        'message': None
    })