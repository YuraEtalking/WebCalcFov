from fastapi import FastAPI

from core.config import settings
from web.routers import web_router


app = FastAPI(title=settings.app_title, description=settings.app_description)
app.include_router(web_router)

