from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from backend.web.templates import render


web_router = APIRouter()


@web_router.get('/', name='index_page', response_class=HTMLResponse)
async def index_page(request: Request):
    return render(request, 'index_page.html')