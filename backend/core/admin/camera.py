from starlette_admin import StringField, IntegerField, BooleanField, DateTimeField, HasMany, EnumField, HasOne
from starlette_admin.contrib.sqla import ModelView

from backend.models import BayonetType


class CameraAdmin(ModelView):
    label = 'Камеры'
    name = 'Камера'

    fields = [
        IntegerField('id', label='ID'),
        StringField('manufacturer', label='Производитель'),
        StringField('name', label='Название'),
        EnumField('bayonet', label='Байонет', enum=BayonetType),
        HasMany('compatible_lenses', label='Совместимые объективы', identity='lens'),
        HasOne('sensor', label='Сенсор', identity='sensor'),

        # Статус и даты создания/редактирования
        BooleanField('is_active', label='Статус'),
        DateTimeField(
            'created_at',
            label='Дата создания записи',
            read_only=True,
        ),
        DateTimeField(
            'updated_at',
            label='Дата обновления записи',
            read_only=True,
        ),
    ]

    exclude_fields_from_list = ['compatible_lenses']
    exclude_fields_from_create = [
        'created_at',
        'updated_at',
        'compatible_lenses',
    ]
    exclude_fields_from_edit = [
        'created_at',
        'updated_at',
        'compatible_lenses',
    ]

    searchable_fields = ['manufacturer', 'name']
    sortable_fields = ['id', 'manufacturer', 'name', 'created_at']