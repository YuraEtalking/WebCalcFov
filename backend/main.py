from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.core.logging_conf import setup_logger
from backend.core.config import settings
from backend.core.admin import setup_admin
from backend.web import cameras, fov, partials, lenses, wiki


logger = setup_logger()
app = FastAPI(title=settings.app_title, description=settings.app_description)
setup_admin(app)
app.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static',
)

app.include_router(fov.web_router)
app.include_router(partials.web_router)
app.include_router(wiki.web_router)
app.include_router(cameras.web_router, prefix='/wiki/{slug}')
app.include_router(lenses.web_router, prefix='/wiki/{slug}')
