from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, HasMany, HasOne, EnumField, DateField
)
from starlette_admin.contrib.sqla import ModelView
from backend.models import SpecLens, BayonetType, ConstructionType


class LensAdmin(ModelView):
    identity = 'lens'
    label = 'Объективы'
    name = 'Объектив'

    fields = [
        # Основное.
        IntegerField('id', label='ID'),
        StringField('manufacturer', label='Производитель'),
        StringField('name', label='Название'),
        EnumField(
            'bayonet',
            label='Байонет',
            enum=BayonetType,
            help_text='Крепление объектива к камере.',
        ),

        # Даты начала и окончания производства.
        DateField(
            'production_start_date',
            label='Дата анонса/начала продаж',
        ),
        DateField(
            'production_end_date',
            label='Дата окончания продаж',
        ),

        # Фокусное.
        FloatField(
            'focal_wide',
            label='Фокусное расстояние в широкоугольном режиме',
            help_text='Если объектив фикс(PRIME), то значение дублируется для '
                      'обоих полей фокусного расстояния.'
        ),
        FloatField(
            'focal_tele',
            label='Фокусное расстояние в теле режиме',
        ),

        # Диафрагма.
        FloatField(
            'aperture_max_wide',
            label='Максимальная диафрагма в широкоугольном режиме',
            help_text='Если объектив фикс(PRIME) или зум(ZOOM) с '
                      'фиксированным значением максимальной диафрагмы, '
                      'то значение дублируется для обоих полей диафрагмы.'
        ),
        FloatField(
            'aperture_max_tele',
            label='Максимальная диафрагма в теле режиме',
        ),

        # Поля связанных моделей.
        HasMany('links', label='Ссылки', identity='link'),
        HasMany(
            'compatible_cameras',
            label='Совместимые камеры',
            identity='camera',
        ),
        HasMany(
            'teleconverters',
            label='Телеконверторы',
            identity='teleconverter',
        ),
        HasOne('spec', label='Спецификации', identity='speclens'),

        # Статус и даты создания/редактирования
        BooleanField(
            'is_active',
            label='Запись активна',
            help_text='Снимите отметку, чтобы отключить запись без удаления.'
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
        'aperture_max_wide', 'focal_wide', 'links',
        'compatible_cameras', 'teleconverters', 'created_at', 'updated_at'
    ]
    exclude_fields_from_create = [
        'created_at',
        'updated_at',
        'spec',
        'links',
        'compatible_cameras',
    ]
    exclude_fields_from_edit = [
        'created_at',
        'updated_at',
        'spec',
        'compatible_cameras',
    ]

    searchable_fields = [
        'manufacturer',
        'name',
        'focal_tele',
        'aperture_max_tele',
    ]
    sortable_fields = [
        'id',
        'manufacturer',
        'name',
        'focal_tele',
        'created_at',
    ]

    async def create(self, request, data):
        """Создаю пустой SpecLens для быстрого перехода со страницы Lens."""
        lens = await super().create(request, data)
        session = request.state.session
        spec = SpecLens(
            lens_id=lens.id,
            name=f'Спецификации: {lens.name}'

        )
        session.add(spec)
        session.commit()

        return lens
