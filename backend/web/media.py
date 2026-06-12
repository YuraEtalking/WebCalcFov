from fastapi import APIRouter
from starlette.responses import FileResponse, JSONResponse, RedirectResponse, StreamingResponse
from sqlalchemy_file.storage import StorageManager
from libcloud.storage.types import ObjectDoesNotExistError
from libcloud.storage.drivers.local import LocalStorageDriver

media_router = APIRouter()


@media_router.get('/medias/{storage}/{file_id}', name='media')
async def serve_media(storage: str, file_id: str):
    try:
        file = StorageManager.get_file(f'{storage}/{file_id}')
    except ObjectDoesNotExistError:
        return JSONResponse({'detail': 'Not found'}, status_code=404)

    if isinstance(file.object.driver, LocalStorageDriver):
        return FileResponse(
            file.get_cdn_url(),
            media_type=file.content_type,
            filename=file.filename,
        )
    if file.get_cdn_url() is not None:
        return RedirectResponse(file.get_cdn_url())

    return StreamingResponse(
        file.object.as_stream(),
        media_type=file.content_type,
    )
