from pathlib import Path

from sqlalchemy_file.storage import StorageManager
from libcloud.storage.drivers.local import LocalStorageDriver

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent  # -> backend/
UPLOADS_DIR = PROJECT_DIR / 'uploads'


def configure_storage() -> None:
    """Создаёт папки для загрузок и регистрирует хранилища файлов."""
    images_dir = UPLOADS_DIR / 'images'
    images_dir.mkdir(parents=True, exist_ok=True)

    # Защита от повторной регистрации (uvicorn --reload, тесты)
    if 'images' in StorageManager._storages:  # noqa: SLF001
        return

    container = LocalStorageDriver(str(UPLOADS_DIR)).get_container('images')
    StorageManager.add_storage('images', container)