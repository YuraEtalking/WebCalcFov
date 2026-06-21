from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from backend.core.logging_conf import setup_logger
from backend.core.config import settings
from backend.core.admin import setup_admin
from backend.core.storage import configure_storage
from backend.web import cameras, fov, partials, lenses, wiki, i18n_middleware, index, tools_list, media_router, compare_router


logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- выполняется при старте приложения ---
    configure_storage()
    yield

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)

setup_admin(app)
app.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static',
)
app.middleware('http')(i18n_middleware)
app.include_router(index.web_router)
app.include_router(compare_router)
app.include_router(tools_list.web_router, prefix='/tools')
app.include_router(fov.web_router, prefix='/fov')
app.include_router(partials.web_router, prefix='/partials')
app.include_router(wiki.web_router, prefix='/wiki')
app.include_router(cameras.web_router, prefix='/wiki/{slug}')
app.include_router(lenses.web_router, prefix='/wiki/{slug}')
app.include_router(media_router)
