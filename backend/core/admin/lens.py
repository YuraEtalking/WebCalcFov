from sqladmin import ModelView

from backend.models import Lens


class LensAdmin(ModelView, model=Lens):
    name = 'Объектив'
    name_plural = 'Объективы'
    icon = 'fa-solid fa-less-than'

    column_list = [
        Lens.id,
        Lens.manufacturer,
        Lens.name,
        Lens.type_lens,
        Lens.bayonet,
        Lens.focal_max,
        Lens.aperture_max,
        Lens.created_at,
        Lens.updated_at,
        Lens.is_active,
    ]
    column_details_list = [
        Lens.manufacturer,
        Lens.name,
        Lens.type_lens,
        Lens.bayonet,
        Lens.focal_min,
        Lens.focal_max,
        Lens.aperture_min,
        Lens.aperture_max,
        Lens.is_active,
        Lens.created_at,
        Lens.updated_at,
        Lens.links,
        'compatible_cameras',
    ]
    column_labels = {
        Lens.id: 'ID',
        Lens.name: 'Название',
        Lens.type_lens: 'Тип объектива',
        Lens.bayonet: 'Байонет',
        Lens.focal_min: 'Минимальное фокусное расстояние',
        Lens.focal_max: 'Максимальное фокусное расстояние',
        Lens.aperture_min: 'Минимальная диафрагма',
        Lens.aperture_max: 'Максимальная диафрагма',
        Lens.compatible_cameras: 'Совместимые камеры',
        Lens.manufacturer: 'Производитель',
        Lens.created_at: 'Дата создания записи',
        Lens.updated_at: 'Дата обновления записи',
        Lens.is_active: 'Статус',
        Lens.links: 'Ссылки',
    }
    column_searchable_list = [
        Lens.manufacturer,
        Lens.name,
        Lens.focal_max,
        Lens.aperture_max,
    ]
    column_sortable_list = [
        Lens.id,
        Lens.manufacturer,
        Lens.name,
        Lens.focal_max,
        Lens.created_at,
    ]
    form_excluded_columns = [
        Lens.created_at,
        Lens.updated_at,
        Lens.camera_lenses,
    ]
