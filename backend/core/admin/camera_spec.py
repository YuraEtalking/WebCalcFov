from starlette_admin import (
    StringField, IntegerField, FloatField, BooleanField,
    DateTimeField, TextAreaField, HasOne, EnumField, JSONField
)
from starlette_admin.contrib.sqla import ModelView
from backend.models import (
    SensorFormat,
    SensorTechnology,
    CameraCategory,
    CameraType,
    MediumType,
    ViewfinderType,
    ScreenType,
    CardType,
)
from loguru import logger
from backend.core.admin.admin_fields import CommaToDotFloatField


class SpecCameraAdmin(ModelView):
    identity = 'spec_camera'
    label = 'Характеристики камеры'
    name = 'Характеристика камеры'

    fields = [
        # === Основное ===
        IntegerField('id', label='ID'),
        StringField('name', label='Название'),
        IntegerField('camera_id', label='ID камеры'),

        # === Тип камеры ===
        EnumField(
            'camera_category',
            label='Категория камеры',
            enum=CameraCategory,
        ),
        EnumField(
            'camera_type',
            label='Тип камеры',
            enum=CameraType,
        ),
        EnumField(
            'medium_type',
            label='Тип носителя',
            enum=MediumType,
        ),

        # === Процессор ===
        StringField('processor', label='Процессор'),

        # === Сенсор ===
        EnumField(
            'sensor_format',
            label='Формат сенсора',
            enum=SensorFormat,
        ),
        EnumField(
            'sensor_technology',
            label='Технология сенсора',
            enum=SensorTechnology,
        ),
        BooleanField(
            'has_global_shutter',
            label='Глобальный затвор',
        ),
        IntegerField(
            'max_raw_bit_depth',
            label='Максимальная битность RAW',
        ),
        FloatField(
            'max_readout_time_ms',
            label='Макс. время считывания, мс',
        ),
        FloatField(
            'sensor_width_mm',
            label='Ширина сенсора, мм',
        ),
        FloatField(
            'sensor_height_mm',
            label='Высота сенсора, мм',
        ),
        IntegerField(
            'sensor_pixels_width',
            label='Ширина сенсора, пикселей',
        ),
        IntegerField(
            'sensor_pixels_height',
            label='Высота сенсора, пикселей',
        ),
        FloatField(
            'effective_megapixels',
            label='Эффективное разрешение, Мп',
        ),
        FloatField(
            'pixel_pitch_um',
            label='Размер пикселя, мкм',
        ),
        StringField(
            'native_aspect_ratio',
            label='Нативное соотношение сторон',
        ),

        # === Стабилизация ===
        BooleanField(
            'has_ibis',
            label='Матричная стабилизация (IBIS)',
        ),
        FloatField(
            'ibis_stops',
            label='Эффективность IBIS, стопов',
        ),

        # === ISO ===
        IntegerField('iso_min', label='Минимальное ISO'),
        IntegerField('iso_max', label='Максимальное ISO'),
        IntegerField(
            'iso_expanded_min',
            label='Расширенное ISO: минимум',
        ),
        IntegerField(
            'iso_expanded_max',
            label='Расширенное ISO: максимум',
        ),
        BooleanField(
            'has_dual_gain',
            label='Dual Gain ISO',
        ),
        StringField(
            'dual_gain_switch_iso',
            label='ISO переключения Dual Gain',
        ),

        # === Затвор ===
        StringField(
            'shutter_speed_min',
            label='Минимальная выдержка',
        ),
        StringField(
            'shutter_speed_max',
            label='Максимальная выдержка',
        ),
        StringField(
            'electronic_shutter_speed_min',
            label='Минимальная выдержка электронного затвора',
        ),
        BooleanField(
            'has_mechanical_shutter',
            label='Механический затвор',
        ),
        StringField(
            'flash_sync_speed',
            label='Выдержка синхронизации вспышки',
        ),

        # === Серийная съёмка ===
        FloatField(
            'burst_fps_mechanical',
            label='Серийная съёмка: механический затвор, fps',
        ),
        FloatField(
            'burst_fps_electronic',
            label='Серийная съёмка: электронный затвор, fps',
        ),
        FloatField(
            'burst_fps_jpg',
            label='Серийная съёмка JPG, fps',
        ),
        FloatField(
            'burst_fps_raw',
            label='Серийная съёмка RAW, fps',
        ),

        # === Буфер ===
        IntegerField(
            'buffer_high_efficiency_raw_jpg_frames',
            label='Буфер HE RAW + JPG, кадров',
        ),
        IntegerField(
            'buffer_lossless_compressed_raw_frames',
            label='Буфер lossless compressed RAW, кадров',
        ),
        IntegerField(
            'buffer_high_efficiency_raw_frames',
            label='Буфер HE RAW, кадров',
        ),

        # === Автофокус ===
        IntegerField(
            'af_points',
            label='Количество точек автофокуса',
        ),
        FloatField(
            'af_detection_range_ev_min',
            label='Минимальная чувствительность AF, EV',
        ),
        BooleanField(
            'has_eye_af',
            label='AF по глазам / лицу / объектам',
        ),
        BooleanField(
            'has_animal_af',
            label='AF по животным / птицам / транспорту',
        ),
        TextAreaField(
            'detected_objects_af',
            label='Распознаваемые объекты AF',
        ),

        # === Видоискатель ===
        EnumField(
            'viewfinder_type',
            label='Тип видоискателя',
            enum=ViewfinderType,
        ),
        IntegerField(
            'viewfinder_resolution_dots',
            label='Разрешение видоискателя, точек',
        ),
        FloatField(
            'viewfinder_magnification',
            label='Увеличение видоискателя',
        ),
        FloatField(
            'viewfinder_coverage_percent',
            label='Покрытие видоискателя, %',
        ),

        # === Экран ===
        FloatField(
            'screen_size_inches',
            label='Диагональ экрана, дюймы',
        ),
        IntegerField(
            'screen_resolution_dots',
            label='Разрешение экрана, точек',
        ),
        EnumField(
            'screen_type',
            label='Тип экрана',
            enum=ScreenType,
        ),
        BooleanField(
            'is_touchscreen',
            label='Сенсорный экран',
        ),

        # === RAW-видео ===
        StringField(
            'raw_video_max_resolution',
            label='Максимальное разрешение RAW-видео',
        ),
        IntegerField(
            'raw_video_max_fps_at_max_resolution',
            label='Макс. fps RAW при максимальном разрешении',
        ),
        IntegerField(
            'raw_video_max_fps',
            label='Максимальный fps RAW-видео',
        ),
        IntegerField(
            'raw_video_max_resolution_at_max_fps',
            label='Разрешение RAW при максимальном fps',
        ),
        IntegerField(
            'raw_video_max_bitrate_mbps',
            label='Максимальный битрейт RAW-видео, Мбит/с',
        ),
        IntegerField(
            'raw_video_max_bit_depth',
            label='Максимальная битность RAW-видео',
        ),
        BooleanField(
            'has_internal_raw_video',
            label='Внутренняя запись RAW-видео',
        ),
        BooleanField(
            'has_external_raw_video',
            label='Внешняя запись RAW-видео',
        ),

        # === Видео / кодеки ===
        BooleanField(
            'has_log_profile',
            label='Поддержка Log-профилей',
        ),
        StringField(
            'video_codecs',
            label='Поддерживаемые видеокодеки',
        ),
        IntegerField(
            'video_max_bit_depth',
            label='Максимальная битность видео',
        ),
        IntegerField(
            'video_max_bitrate_mbps',
            label='Максимальный битрейт видео, Мбит/с',
        ),

        # === Карты памяти ===
        IntegerField(
            'card_slots',
            label='Количество слотов карт памяти',
        ),
        EnumField(
            'card_types',
            label='Поддерживаемые типы карт памяти',
            enum=CardType,
            multiple=True,
        ),

        # === Интерфейсы и связь ===
        BooleanField('has_wifi', label='Wi‑Fi'),
        BooleanField('has_bluetooth', label='Bluetooth'),
        BooleanField('has_gps', label='GPS'),
        StringField('usb_type', label='Тип USB'),
        BooleanField(
            'has_headphone_jack',
            label='Выход для наушников',
        ),
        BooleanField(
            'has_microphone_jack',
            label='Микрофонный вход',
        ),
        StringField('hdmi_type', label='Тип HDMI'),

        # === Питание ===
        StringField(
            'battery_model',
            label='Модель аккумулятора',
        ),
        IntegerField(
            'battery_life_shots_cipa',
            label='Ресурс аккумулятора по CIPA, кадров',
        ),
        BooleanField(
            'has_usb_charging',
            label='Зарядка по USB',
        ),

        # === Корпус ===
        IntegerField(
            'weight_g',
            label='Вес, г',
        ),
        FloatField('width_mm', label='Ширина, мм'),
        FloatField('height_mm', label='Высота, мм'),
        FloatField('depth_mm', label='Глубина, мм'),
        BooleanField(
            'is_weather_sealed',
            label='Пыле- и влагозащита',
        ),
        BooleanField(
            'has_built_in_flash',
            label='Встроенная вспышка',
        ),
    ]

    exclude_fields_from_list = [
        'camera_id',

        'camera_category',
        'camera_type',
        'medium_type',

        'processor',

        'sensor_format',
        'sensor_technology',
        'has_global_shutter',
        'max_raw_bit_depth',
        'max_readout_time_ms',
        'sensor_width_mm',
        'sensor_height_mm',
        'sensor_pixels_width',
        'sensor_pixels_height',
        'effective_megapixels',
        'pixel_pitch_um',
        'native_aspect_ratio',

        'has_ibis',
        'ibis_stops',

        'iso_min',
        'iso_max',
        'iso_expanded_min',
        'iso_expanded_max',
        'has_dual_gain',
        'dual_gain_switch_iso',

        'shutter_speed_min',
        'shutter_speed_max',
        'electronic_shutter_speed_min',
        'has_mechanical_shutter',
        'flash_sync_speed',

        'burst_fps_mechanical',
        'burst_fps_electronic',
        'burst_fps_jpg',
        'burst_fps_raw',

        'buffer_high_efficiency_raw_jpg_frames',
        'buffer_lossless_compressed_raw_frames',
        'buffer_high_efficiency_raw_frames',

        'af_points',
        'af_detection_range_ev_min',
        'has_eye_af',
        'has_animal_af',
        'detected_objects_af',

        'viewfinder_type',
        'viewfinder_resolution_dots',
        'viewfinder_magnification',
        'viewfinder_coverage_percent',

        'screen_size_inches',
        'screen_resolution_dots',
        'screen_type',
        'is_touchscreen',

        'raw_video_max_resolution',
        'raw_video_max_fps_at_max_resolution',
        'raw_video_max_fps',
        'raw_video_max_resolution_at_max_fps',
        'raw_video_max_bitrate_mbps',
        'raw_video_max_bit_depth',
        'has_internal_raw_video',
        'has_external_raw_video',

        'has_log_profile',
        'video_codecs',
        'video_max_bit_depth',
        'video_max_bitrate_mbps',

        'card_slots',
        'card_types',

        'has_wifi',
        'has_bluetooth',
        'has_gps',
        'usb_type',
        'has_headphone_jack',
        'has_microphone_jack',
        'hdmi_type',

        'battery_model',
        'battery_life_shots_cipa',
        'has_usb_charging',

        'weight_g',
        'width_mm',
        'height_mm',
        'depth_mm',
        'is_weather_sealed',
        'has_built_in_flash',
    ]