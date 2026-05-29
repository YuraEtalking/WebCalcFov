from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, HasMany, HasOne, EnumField
)
from starlette_admin.contrib.sqla import ModelView

from loguru import logger


class SpecLensAdmin(ModelView):
    identity = 'speclens'
    label = 'Характеристики объективов'
    name = 'Характеристика объектива'

    fields = [
        StringField('name', label='Название'),
        IntegerField('id', label='ID'),
        IntegerField('diameter', label='Диаметр объектива'),
        FloatField('min_aperture', label='Минимальная диафрагма'),
        StringField(
            'angle_of_view_tele_ff_display',
            label='Угол обзора tele FF',
            read_only=True,
        ),
        BooleanField('is_active', label='Статус'),
        HasOne('lens', label='Объектив', identity='lens'),
    ]

    exclude_fields_from_list = [
        'diameter',
    ]
    exclude_fields_from_create = [
        'angle_of_view_tele_ff_display',

    ]
    exclude_fields_from_edit = [
        'angle_of_view_tele_ff_display',

    ]