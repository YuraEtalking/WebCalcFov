from sqladmin import ModelView

from backend.models import Lens



class LensAdmin(ModelView, model=Lens):
    name = 'Объектив'
    name_plural = 'Объективы'

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
        'compatible_cameras'
    ]
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
