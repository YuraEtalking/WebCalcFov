from starlette_admin import HasOne, EnumField
from starlette_admin.contrib.sqla import ModelView

from backend.models import CompatibilityType


class CameraLensAdmin(ModelView):
    label = 'Совместимости камер и объективов'
    name = 'Совместимость камеры и объектива'

    fields = [
        HasOne('camera', label='Камера', identity='camera'),
        HasOne('lens', label='Объектив', identity='lens'),
        EnumField(
            'type_lens',
            label='Тип подключения',
            enum=CompatibilityType,
            help_text='Выберите тип подключения прямое соединение(DIRECT) или '
                      'переходник(WITH_CONVERTOR).'
        ),
    ]

    searchable_fields = ['camera.name', 'lens.name']
    sortable_fields = ['camera.name', 'lens.name']