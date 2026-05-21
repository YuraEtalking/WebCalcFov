from sqladmin import ModelView

from backend.models import Link


class LinkAdmin(ModelView, model=Link):
    name = 'Ссылка'
    name_plural = 'Ссылки'
    icon = 'fa-solid fa-link'

    column_list = [
        Link.id,
        Link.title,
        Link.url,
        Link.lenses,
    ]

    form_columns = [
        Link.title,
        Link.url,
        Link.description,
        Link.lenses,
    ]

    column_labels = {
        Link.id: 'ID',
        Link.title: 'Название',
        Link.url: 'URL',
        Link.description: 'Описание',
        Link.lenses: 'Объектив',
    }