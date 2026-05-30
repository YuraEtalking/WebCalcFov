from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, HasMany, HasOne, EnumField
)
from starlette_admin.contrib.sqla import ModelView
from backend.models import SpecLens, BayonetType, ConstructionType, LensType
from loguru import logger


class SpecLensAdmin(ModelView):
    identity = 'speclens'
    label = 'Характеристики объективов'
    name = 'Характеристика объектива'

    fields = [
        StringField('name', label='Название'),
        IntegerField('id', label='ID'),

        # Конструкция и тип объектива
        EnumField(
            'lens_type',
            label='Тип объектива',
            enum=LensType,
            help_text='Выберите тип объектива.',
        ),
        StringField('construction_type', label='Конструкция'),

        # Физические данные
        IntegerField('weight_g', label='Вес грамм'),
        IntegerField('length_mm', label='Длинна объектива в мм'),
        IntegerField('diameter_mm', label='Диаметр объектива в мм'),

        # Формат покрытия матрицы
        StringField(
            'coverage_format',
            label='Формат объектива',
            help_text='Под какой размер сенсора спроектирован объектив.',
        ),

        # Диафрагма
        FloatField('min_aperture', label='Минимальная диафрагма'),
        IntegerField('aperture_blades', label='Кол-во лепестков диафрагмы'),
        IntegerField(
            'type_diaphragm',
            label='Тип диафрагмы',
            help_text='Например электронная. electronic, mechanical, manual, camera-controlled',
        ),

        StringField(
            'angle_of_view_tele_ff_display',
            label='Угол обзора tele FF',
            read_only=True,
        ),
        BooleanField('is_active', label='Статус'),
        HasOne('lens', label='Объектив', identity='lens'),
    ]

    exclude_fields_from_list = [
        'diameter_mm', 'min_aperture', 'angle_of_view_tele_ff_display',
    ]
    exclude_fields_from_create = [
        'angle_of_view_tele_ff_display', 'construction_type',

    ]
    exclude_fields_from_edit = [
        'angle_of_view_tele_ff_display', 'construction_type',

    ]