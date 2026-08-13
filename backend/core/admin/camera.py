from starlette_admin import StringField, IntegerField, BooleanField, DateTimeField, HasMany, EnumField, HasOne
from starlette_admin.contrib.sqla import ModelView

from backend.models import BayonetType, SpecCamera


class CameraAdmin(ModelView):
    label = 'Камеры'
    name = 'Камера'

    fields = [
        IntegerField('id', label='ID'),
        StringField('manufacturer', label='Производитель'),
        StringField('name', label='Название'),
        EnumField('bayonet', label='Байонет', enum=BayonetType),

        # Поля связанных моделей.
        HasMany('links', label='Ссылки', identity='link'),
        HasMany(
            'compatible_lenses',
            label='Совместимые объективы',
            identity='lens'
        ),
        HasOne('spec', label='Спецификации', identity='spec_camera'),

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

    exclude_fields_from_list = ['compatible_lenses', 'spec']
    exclude_fields_from_create = [
        'created_at',
        'updated_at',
        'compatible_lenses', 'spec',
    ]
    exclude_fields_from_edit = [
        'created_at',
        'updated_at',
        'compatible_lenses', 'spec',
    ]

    searchable_fields = ['manufacturer', 'name']
    sortable_fields = ['id', 'manufacturer', 'name', 'created_at']


    async def create(self, request, data):
        """Создаю пустой SpecCamera для быстрого перехода со страницы Camera."""
        camera = await super().create(request, data)
        session = request.state.session
        spec = SpecCamera(
            camera_id=camera.id,
            name=f'Спецификации: {camera.name}'

        )
        session.add(spec)
        session.commit()

        return camera