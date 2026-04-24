from sqladmin import ModelView

from backend.models import Camera



class CameraAdmin(ModelView, model=Camera):
    name = 'Камера'
    name_plural = 'Камеры'
    icon = 'fa-solid fa-camera'

    column_list = [
        Camera.id,
        Camera.manufacturer,
        Camera.name,
        Camera.bayonet,
        Camera.created_at,
        Camera.updated_at,
        Camera.is_active,
    ]
    column_labels = {
        Camera.id: 'ID',
        Camera.name: 'Название',
        Camera.bayonet: 'Байонет',
        Camera.compatible_lenses: 'Совместимые объективы',
        Camera.manufacturer: 'Производитель',
        Camera.created_at: 'Дата создания записи',
        Camera.updated_at: 'Дата обновления записи',
        Camera.is_active: 'Статус',
    }
    column_details_list = [
        Camera.id,
        Camera.manufacturer,
        Camera.name,
        Camera.bayonet,
        Camera.created_at,
        Camera.updated_at,
        Camera.is_active,
        'compatible_lenses',
    ]
    column_searchable_list = [Camera.manufacturer, Camera.name]
    column_sortable_list = [
        Camera.id,
        Camera.manufacturer,
        Camera.name,
        Camera.created_at,
    ]
    form_excluded_columns = [
        Camera.created_at,
        Camera.updated_at,
        Camera.camera_lenses,
    ]