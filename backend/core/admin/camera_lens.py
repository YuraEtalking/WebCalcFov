from sqladmin import ModelView

from backend.models import CameraLens


class CameraLensAdmin(ModelView, model=CameraLens):
    name = 'Совместимость камеры и объектива'
    name_plural = 'Совместимости камер и объективов'

    column_list = [
        CameraLens.camera,
        CameraLens.lens,
        CameraLens.convertor,
    ]