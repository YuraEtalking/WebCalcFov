from starlette_admin import IntegerField, BooleanField, DateTimeField, StringField, HasMany, HasOne, EnumField
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.contrib.sqla.fields import ImageField

from backend.models import ImageRole

from pathlib import Path


class ImageAdmin(ModelView):
    identity = 'image'
    label = 'Изображения'
    name = 'Изображение'

    fields = [
        IntegerField('id', label='ID'),
        ImageField('file', label='Изображение'),
        StringField('title', label='Название'),
        StringField('alt', label='Альтернативное описание'),
        HasMany(
            'lens_links',
            label='Связанные сущности',
            identity='lens_image_link',
            help_text='Показывает где используется фото.'
        ),

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
        'alt', 'created_at', 'updated_at',
    ]
    exclude_fields_from_create = [
        'lens_links',
        'created_at',
        'updated_at',
    ]
    exclude_fields_from_edit = [
        'created_at',
        'updated_at',
    ]


class LensImageLinkAdmin(ModelView):
    identity = 'lens_image_link'
    label = 'Связь фото и линзы'
    name = 'Связь фото и линзы'

    fields = [
        HasOne('lens', label='линза', identity='lens'),
        HasOne('image', label='фото', identity='image'),
        EnumField(
            'role',
            label='Тип фото',
            enum=ImageRole,
        ),
    ]
