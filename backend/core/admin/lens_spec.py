from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, HasMany, HasOne, EnumField
)
from starlette_admin.contrib.sqla import ModelView
from backend.models import (
    FilterMountType,
    LensType,
    SensorFormat,
    TypeDiaphragm
)
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
        EnumField(
            'coverage_format',
            label='Формат объектива',
            enum=SensorFormat,
            help_text='Под какой размер сенсора спроектирован объектив.',
        ),


        # Диафрагма
        FloatField('min_aperture', label='Минимальная диафрагма'),
        IntegerField('aperture_blades', label='Кол-во лепестков диафрагмы'),
        EnumField(
            'type_diaphragm',
            label='Тип диафрагмы',
            enum=TypeDiaphragm,
            help_text='Например электронная. electronic, mechanical, manual, camera-controlled',
        ),
        BooleanField(
            'aperture_blades_rounded',
            label='Скругление лепестков диафрагмы',
        ),


        # Фильтры
        IntegerField('filter_size_mm', label='Размер фильтра мм'),
        BooleanField(
            'supports_front_filters',
            label='Переднее крепление фильтра',
        ),
        BooleanField(
            'rear_filter_holder',
            label='Заднее крепление фильтра',
        ),
        EnumField(
            'filter_mount_type',
            label='Тип крепления фильтра',
            enum=FilterMountType,
        ),


        # Углы обзора объектива
        StringField(
            'angle_of_view_wide',
            label='Угол обзора для широкоугольного положения',
            read_only=True,
        ),
        StringField(
            'angle_of_view_tele',
            label='Угол обзора для теле положения',
            read_only=True,
        ),
        HasOne('lens', label='Объектив', identity='lens'),

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

    exclude_fields_from_list = [
        'diameter_mm',
        'min_aperture',
        'angle_of_view_wide_display',
        'angle_of_view_tele_display',
    ]
    exclude_fields_from_create = [
        'angle_of_view_wide_display',
        'angle_of_view_tele_display',
        'construction_type',
    ]
    exclude_fields_from_edit = [
        'angle_of_view_wide_display',
        'angle_of_view_tele_display',
        'construction_type',
    ]