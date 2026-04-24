from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import ValidationError


web_router = APIRouter()

templates = Jinja2Templates(directory='templates')

@web_router.get('/', response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse('form.html', {
        'request': request,
        'message': None
    })

@web_router.post('/', response_class=HTMLResponse)
async def submit_form(
    request: Request,
        camera: str = Form(...),
        lens: str = Form(...),
        sensor: str = Form(...),
        distance: str = Form(...),
):

    data = {
        'camera': camera,
        'lens': lens,
        'sensor': sensor,
        'distance': distance,
    }

    return templates.TemplateResponse(
        'result.html',
        {
            'request': request,
            'data': data,
        }
    )