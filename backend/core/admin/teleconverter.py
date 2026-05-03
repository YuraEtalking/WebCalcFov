from sqladmin import ModelView

from backend.models import  Teleconverter


class TeleconverterAdmin(ModelView, model=Teleconverter):
    name = 'Телеконвертор'
    name_plural = 'Телеконверторы'
    icon = 'fa-solid fa-less-than'

    column_list = [
        Teleconverter.id,
        Teleconverter.manufacturer,
        Teleconverter.name,
        Teleconverter.bayonet,
        Teleconverter.multiplier,
        Teleconverter.created_at,
        Teleconverter.updated_at,
        Teleconverter.is_active,
        Teleconverter.lenses,
    ]
    column_details_list = [
        Teleconverter.id,
        Teleconverter.manufacturer,
        Teleconverter.name,
        Teleconverter.bayonet,
        Teleconverter.multiplier,
        Teleconverter.created_at,
        Teleconverter.updated_at,
        Teleconverter.is_active,
        Teleconverter.lenses,
    ]
    column_labels = {
        Teleconverter.id: 'ID',
        Teleconverter.name: 'Название',
        Teleconverter.bayonet: 'Байонет',
        Teleconverter.multiplier: 'Увеличение фокусного расстояния',
        Teleconverter.manufacturer: 'Производитель',
        Teleconverter.created_at: 'Дата создания записи',
        Teleconverter.updated_at: 'Дата обновления записи',
        Teleconverter.is_active: 'Статус',
    }
    column_searchable_list = [
        Teleconverter.manufacturer,
        Teleconverter.name,
    ]
    column_sortable_list = [
        Teleconverter.id,
        Teleconverter.manufacturer,
        Teleconverter.name,
        Teleconverter.multiplier,
        Teleconverter.created_at,
    ]
    form_excluded_columns = [
        Teleconverter.created_at,
        Teleconverter.updated_at,
    ]