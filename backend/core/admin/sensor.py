from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField, DateTimeField, EnumField,
)
from starlette_admin.contrib.sqla import ModelView


class SensorAdmin(ModelView):
    label = 'Сенсоры'
    name = 'Сенсор'

    fields = [
        IntegerField('id', label='ID'),
        StringField('manufacturer', label='Производитель'),
        StringField('name', label='Название'),
        FloatField('width', label='Ширина мм'),
        FloatField('height', label='Высота мм'),
        FloatField(
            'crop_factor',
            label='Кроп-фактор',
            read_only=True,
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
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

    exclude_fields_from_create = ['created_at', 'updated_at']
    exclude_fields_from_edit = ['created_at', 'updated_at']

    searchable_fields = ['sensor_type']
    sortable_fields = ['id', 'created_at']

    # Форматтеры в Starlette-Admin реализуются через переопределение метода
    async def serialize_field_value(self, value, field, action, request):
        if field.name == 'width' and value is not None:
            return f'{value:.1f}'
        if field.name == 'height' and value is not None:
            return f'{value:.1f}'
        if field.name == 'crop_factor' and value is not None:
            return f'{value:.2f}'
        return await super().serialize_field_value(value, field, action, request)
