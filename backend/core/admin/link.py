from starlette_admin import StringField, IntegerField, HasMany, BooleanField, DateTimeField
from starlette_admin.contrib.sqla import ModelView


class LinkAdmin(ModelView):
    label = 'Ссылки'
    name = 'Ссылка'

    fields = [
        IntegerField('id', label='ID'),
        StringField('title', label='Название'),
        StringField('url', label='URL'),
        StringField('description', label='Описание'),
        HasMany('lenses', label='Объективы', identity='lens'),

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
        'url', 'description',
    ]
    exclude_fields_from_create = [
        'created_at', 'updated_at',
    ]
    exclude_fields_from_edit = [
        'created_at', 'updated_at',
    ]

    searchable_fields = ['title', 'url']
    sortable_fields = ['id', 'title']