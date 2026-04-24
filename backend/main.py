from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.core.config import settings
from backend.core.admin import setup_admin
from backend.web.routers import web_router



app = FastAPI(title=settings.app_title, description=settings.app_description)
app.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static',
)
setup_admin(app)
app.include_router(web_router)

