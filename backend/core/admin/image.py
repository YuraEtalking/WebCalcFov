from starlette_admin import IntegerField, BooleanField, DateTimeField, StringField, HasMany, HasOne, EnumField
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.contrib.sqla.fields import ImageField

from backend.models import ImageRole
from .services import get_exif
import io
from PIL import Image as PILImage

from loguru import logger


class ImageAdmin(ModelView):
    identity = 'image'
    label = 'Изображения'
    name = 'Изображение'

    fields = [
        IntegerField('id', label='ID'),
        ImageField('file', label='Изображение'),
        StringField('title', label='Название'),
        StringField('alt', label='Альтернативное описание'),

        # Данные Exif
        StringField('photographer_name', label='Фотограф'),
        IntegerField('iso', label='ISO'),
        StringField('shutter_speed', label='Выдержка'),
        StringField('aperture', label='Диафрагма'),
        StringField('focal_length', label='фокусное расстояние'),
        StringField('camera_model_name', label='Модель камеры'),
        StringField('lens_model_name', label='Модель объектива'),

        # Поля связанных моделей.
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
        'updated_at', 'photographer_name', 'iso', 'shutter_speed', 'aperture', 'focal_length', 'camera_model_name', 'lens_model_name'
    ]
    exclude_fields_from_edit = [
        'created_at',
        'updated_at',
    ]

    def _extract_exif_from_upload(self, file) -> dict:
        """Читает EXIF из загруженного файла (UploadFile), не сохраняя его на диск."""
        if isinstance(file, (list, tuple)):
            if not file:
                return {}
            upload = file[0]
        else:
            upload = file

        starlette_file = getattr(upload, 'file', None) or upload

        try:
            pos = None
            if hasattr(starlette_file, 'tell'):
                pos = starlette_file.tell()

            if hasattr(starlette_file, 'seek'):
                starlette_file.seek(0)

            raw = starlette_file.read()

            if hasattr(starlette_file, 'seek'): # указатель на место
                starlette_file.seek(pos if pos is not None else 0)

            with PILImage.open(io.BytesIO(raw)) as img:
                return get_exif(img)

        except Exception as e:
            logger.warning('Не удалось прочитать EXIF: {}', e)
            return {}

    async def create(self, request, data):
        """Создание новой записи. Достаём EXIF и кладём в request.state."""
        file = data.get('file')
        if file:
            request.state._exif = self._extract_exif_from_upload(file)
            logger.debug('EXIF извлечён: {}', request.state._exif)
        return await super().create(request, data)

    async def before_create(self, request, data, obj):
        """
        Вызывается перед сохранением объекта в БД.
        Здесь obj — это уже готовый объект Image.
        Записываем в него EXIF-поля.
        """
        exif = getattr(request.state, '_exif', None)
        if exif:
            for key, value in exif.items():
                setattr(obj, key, value)
            logger.debug('EXIF записан в объект: iso={}', obj.iso)

    async def edit(self, request, pk, data):
        """Редактирование. Если загрузили новый файл — обновляем EXIF."""
        file = data.get('file')
        if file and not isinstance(file, str):
            request.state._exif = self._extract_exif_from_upload(file)
            logger.debug('EXIF при редактировании: {}', request.state._exif)
        return await super().edit(request, pk, data)

    async def before_edit(self, request, data, obj):
        """Записываем обновлённый EXIF в объект при редактировании."""
        exif = getattr(request.state, '_exif', None)
        if exif:
            for key, value in exif.items():
                setattr(obj, key, value)




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
