from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, HasMany, EnumField
)
from starlette_admin.contrib.sqla import ModelView

from backend.models import SpecLens, BayonetType, ConstructionType


class TeleconverterAdmin(ModelView):
    label = 'Телеконверторы'
    name = 'Телеконвертор'

    fields = [
        IntegerField('id', label='ID'),
        StringField('manufacturer', label='Производитель'),
        StringField('name', label='Название'),
        EnumField('bayonet', label='Байонет', enum=BayonetType),
        FloatField('multiplier', label='Увеличение фокусного расстояния'),
        BooleanField('is_active', label='Статус'),
        DateTimeField('created_at', label='Дата создания записи', read_only=True),
        DateTimeField('updated_at', label='Дата обновления записи', read_only=True),
        HasMany('lenses', label='Объективы', identity='lens'),
    ]

    exclude_fields_from_create = ['created_at', 'updated_at']
    exclude_fields_from_edit = ['created_at', 'updated_at']

    searchable_fields = ['manufacturer', 'name']
    sortable_fields = ['id', 'manufacturer', 'name', 'multiplier', 'created_at']