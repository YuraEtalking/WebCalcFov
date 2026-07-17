from typing import Any

from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, TextAreaField, HasOne, EnumField
)
from starlette.requests import Request
from starlette_admin.exceptions import FormValidationError
from starlette_admin.contrib.sqla import ModelView
from backend.models import (
    FilterMountType,
    LensType,
    SensorFormat,
    TypeDiaphragm,
    FocusType,
    AutofocusMotorType,ZoomType
)
from loguru import logger
from backend.core.admin.admin_fields import CommaToDotFloatField


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
        IntegerField('weight_g', label='Вес, грамм'),
        IntegerField('length_mm', label='Длинна объектива, мм'),
        IntegerField('diameter_mm', label='Диаметр объектива, мм'),


        # Формат покрытия матрицы
        EnumField(
            'coverage_format',
            label='Формат объектива',
            enum=SensorFormat,
            help_text='Под какой размер сенсора спроектирован объектив.',
        ),


        # Диафрагма
        CommaToDotFloatField('min_aperture', label='Минимальная диафрагма'),
        IntegerField('aperture_blades', label='Кол-во лепестков диафрагмы'),
        EnumField(
            'type_diaphragm',
            label='Тип диафрагмы',
            enum=TypeDiaphragm,
        ),
        BooleanField(
            'aperture_blades_rounded',
            label='Скругление лепестков диафрагмы',
        ),


        # Фильтры
        IntegerField('filter_size_mm', label='Размер фильтра, мм'),
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


        # Фокусировка
        EnumField(
            'focus_type',
            label='Тип/конструкция фокусировки объектива',
            enum=FocusType,
        ),
        BooleanField('autofocus', label='Автофокус'),
        BooleanField(
            'full_time_manual_focus',
            label='Постоянная ручная фокусировка A/M или М/А',
        ),
        CommaToDotFloatField(
            'min_focus_distance_m',
            label='Минимальная дистанция фокусировки, м',
        ),
        EnumField(
            'autofocus_motor_type',
            label='Тип мотора фокусировки',
            enum=AutofocusMotorType,
        ),
        StringField(
            'brand_name_autofocus',
            label='Брендовое название автофокуса',
        ),


        # Стабилизация
        BooleanField('image_stabilization', label='Наличие стабилизатора'),
        StringField(
            'stabilization_name',
            label='Брендовое название стабилизатора',
        ),
        FloatField(
            'stabilization_stops',
            label='Кол-во стопов стабилизации',
        ),


        # Зум
        EnumField(
            'zoom_type',
            label='Тип изменения фокусного расстояния',
            enum=ZoomType,
        ),
        BooleanField('internal_zoom', label='Внутренний зум'),
        BooleanField('zoom_lock', label='Фиксатор зума'),


        # Макро-возможности
        BooleanField('is_macro', label='Макро объектив'),
        FloatField(
            'max_magnification',
            label='Коэффициент увеличения (масштаб съёмки)',
            help_text='Насколько крупно объектив может снять мелкий объект с '
                      'минимальной дистанции фокусировки. '
                      '0.10x - 0.15x : обычный объектив, '
                      '1.0x - 2.0x: настоящее макро 1:1 и более.',
        ),


        # Углы обзора объектива, вычисляемые поля.
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


        # Бленда и аксессуары
        StringField('hood_model', label='Модель бленды'),
        BooleanField('hood_included', label='Бленда в комплекте'),
        BooleanField(
            'tripod_collar_included',
            label='Штативное кольцо в комплекте',
        ),
        BooleanField(
            'tripod_collar_removable',
            label='Съёмное штативное кольцо',
        ),
        BooleanField('case_included', label='Чехол в комплекте'),


        # Комплект поставки
        TextAreaField('supplied_accessories', label='Комплект поставки'),


        # Дополнительно
        BooleanField('weather_sealing', label='Погодозащита'),
        BooleanField('dust_moisture_resistant',
                     label='Защита от пыли и влаги'),
        BooleanField('fluorine_coating', label='Фтористое покрытие'),


        # Статус и даты создания/редактирования
        BooleanField(
            'is_active',
            label='Запись активна',
        ),
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
        'lens_type',
        'autofocus',
        'image_stabilization',
        'construction_type',
        'weight_g',
        'length_mm',
        'diameter_mm',
        'coverage_format',
        'min_aperture',
        'aperture_blades',
        'type_diaphragm',
        'aperture_blades_rounded',
        'filter_size_mm',
        'supports_front_filters',
        'rear_filter_holder',
        'filter_mount_type',
        'focus_type',
        'full_time_manual_focus',
        'min_focus_distance_m',
        'autofocus_motor_type',
        'brand_name_autofocus',
        'stabilization_name',
        'stabilization_stops',
        'zoom_type',
        'internal_zoom',
        'zoom_lock',
        'is_macro',
        'max_magnification',
        'angle_of_view_wide',
        'angle_of_view_tele',
        'hood_model',
        'hood_included',
        'tripod_collar_included',
        'tripod_collar_removable',
        'case_included',
        'supplied_accessories',
        'weather_sealing',
        'dust_moisture_resistant',
        'fluorine_coating',
    ]
    exclude_fields_from_create = [
        'angle_of_view_wide',
        'angle_of_view_tele',
        'construction_type', 'created_at', 'updated_at', 'is_active',
    ]
    exclude_fields_from_edit = [
        'angle_of_view_wide',
        'angle_of_view_tele',
        'construction_type', 'created_at', 'updated_at', 'is_active', 'lens'
    ]