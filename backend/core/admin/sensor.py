from sqladmin import ModelView

from backend.models import Sensor


class SensorAdmin(ModelView, model=Sensor):
    name = 'Сенсор'
    name_plural = 'Сенсоры'

    column_list = [
        Sensor.id,
        Sensor.sensor_type,
        'width',
        'height',
        'crop_factor',
        Sensor.created_at,
        Sensor.updated_at,
        Sensor.is_active,
    ]
    column_searchable_list = [Sensor.sensor_type,]
    column_sortable_list = [
        Sensor.id,
        Sensor.created_at,
    ]
    form_excluded_columns = [
        Sensor.created_at,
        Sensor.updated_at,
    ]
    column_formatters = {
        'width': lambda m, a: f'{m.width:.1f} mm',
        'height': lambda m, a: f'{m.height:.1f} mm',
        'crop_factor': lambda m, a: f'{m.crop_factor:.2f}',
    }
