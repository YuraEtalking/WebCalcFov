from starlette_admin import StringField, IntegerField, HasMany, BooleanField
from starlette_admin.contrib.sqla import ModelView


class LinkAdmin(ModelView):
    label = 'Ссылки'
    name = 'Ссылка'

    fields = [
        IntegerField('id', label='ID'),
        StringField('title', label='Название'),
        StringField('url', label='URL'),
        StringField('description', label='Описание'),
        BooleanField('is_active', label='Статус'),
        HasMany('lenses', label='Объективы', identity='lens'),
    ]

    exclude_fields_from_list = [
        'url', 'description',
    ]

    searchable_fields = ['title', 'url']
    sortable_fields = ['id', 'title']