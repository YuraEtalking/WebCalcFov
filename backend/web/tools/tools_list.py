from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from sqlalchemy import select, union
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.models import Camera, Lens
from backend.web.templates import render


web_router = APIRouter(tags=['Tools'],)


@web_router.get('/', name='tools', response_class=HTMLResponse)
async def tools(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    return render(request,'tools/tools_list.html')