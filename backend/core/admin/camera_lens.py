from sqladmin import ModelView

from backend.models import CameraLens, Camera, Lens


class CameraLensAdmin(ModelView, model=CameraLens):
    name = 'Совместимость камеры и объектива'
    name_plural = 'Совместимости камер и объективов'
    icon = 'fa-solid fa-puzzle-piece'

    column_list = [
        CameraLens.camera,
        CameraLens.lens,
        CameraLens.convertor,
    ]
    column_labels = {
        CameraLens.camera: 'Камера',
        CameraLens.lens: 'Объектив',
        CameraLens.convertor: 'Метод подключения',
    }
# todo нужно добавить поиск и сортировку.