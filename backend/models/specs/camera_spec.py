import math
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, ForeignKey, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    NameFieldsMixin,
    TimeFieldsMixin,
)
from backend.core.constants.sensor_constants import FULL_FRAME_DIAGONAL
from backend.services.fov_calculator import get_degrees_fov
from backend.models.specs.spec_mixins import CameraPhysicalSpecMixin
from backend.models.specs.utils import positive_checks
from backend.models.enums import (
    CameraCategory,
    CameraType,
    SensorFormat,
    MediumType,
    ViewfinderType,
    ScreenType,
)


if TYPE_CHECKING:
    from models.camera import Camera



class SpecCamera(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    Base,
    TimeFieldsMixin,
    NameFieldsMixin,
    CameraPhysicalSpecMixin
):
    """Модель технических спецификаций камеры.

    Все поля характеристик должны быть nullable=True, объект SpecCamera
    создается вместе с объектом Camera, так как ограничение админки не позволяет
    наполнить объект SpecCamera данными сразу вместе с Camera."""

    camera_id: Mapped[int] = mapped_column(
        ForeignKey('camera.id'),
        unique=True,
        nullable=False,
    )

    camera: Mapped['Camera'] = relationship(back_populates='spec',)


    # Тип камеры
    camera_category: Mapped[CameraCategory] = mapped_column(
        Enum(CameraCategory, name='camera_category_enum'),
        nullable=False,
        default=CameraCategory.PHOTO,
    )

    camera_type: Mapped[CameraType] = mapped_column(
        Enum(CameraType, name='camera_type_enum'),
        nullable=False,
        default=CameraType.MIRRORLESS,
    )

    medium_type: Mapped[MediumType] = mapped_column(
        Enum(MediumType, name='medium_type_enum'),
        nullable=False,
        default=MediumType.DIGITAL,
    )


    # Процессор
    processor: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )


    # Сенсор
    sensor_format: Mapped[SensorFormat] = mapped_column(
        Enum(SensorFormat, name='sensor_format_enum'),
        nullable=False,
        default=SensorFormat.FULL_FRAME,
    )

    sensor_width_mm: Mapped[float] = mapped_column(Float)
    sensor_height_mm: Mapped[float] = mapped_column(Float)

    sensor_pixels_width: Mapped[int] = mapped_column(Integer)
    sensor_pixels_height: Mapped[int] = mapped_column(Integer)

    effective_megapixels: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    pixel_pitch_um: Mapped[float | None] = mapped_column(Float, nullable=True) # todo может сделать вычисляемое?

    @property
    def crop_factor(self) -> float:
        diagonal = math.sqrt(
            self.sensor_width_mm ** 2 + self.sensor_height_mm ** 2
        )
        return FULL_FRAME_DIAGONAL / diagonal


    # Стабилизация
    has_ibis: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    ibis_stops: Mapped[float | None] = mapped_column(Float, nullable=True)


    # ISO
    iso_min: Mapped[int | None] = mapped_column(Integer, nullable=True)

    iso_max: Mapped[int | None] = mapped_column(Integer, nullable=True)

    iso_expanded_min: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    iso_expanded_max: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    has_dual_gain: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    dual_gain_switch_iso: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )


    # Затвор
    shutter_speed_min: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Минимальная выдержка

    shutter_speed_max: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Максимальная выдержка

    electronic_shutter_speed_min: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Мин. выдержка электронного затвора

    has_mechanical_shutter: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )

    flash_sync_speed: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )


    # Серийная съёмка
    burst_fps_mechanical: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    burst_fps_electronic: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    burst_fps_jpg: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    burst_fps_raw: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )


    # Буфер
    buffer_high_efficiency_raw_jpg_frames: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Высокоэффективное сжатие RAW + JPG

    buffer_lossless_compressed_raw_frames: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Без сжатия RAW

    buffer_high_efficiency_raw_frames: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Высокоэффективное сжатие RAW


    # Автофокус
    af_points: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Количество точек автофокуса

    af_detection_range_ev_min: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Чувствительность AF в EV

    has_eye_af: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Распознавание глаз/лица/объекты

    has_animal_af: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Распознавание животных/птиц/транспорта

    detected_objects_af: Mapped[str | None] = mapped_column(
        Text, nullable=True
    ) # Объекты которые камера умеет распознавать


    # Видоискатель
    viewfinder_type: Mapped[ViewfinderType | None] = mapped_column(
        Enum(ViewfinderType, name='viewfinder_type_enum'), nullable=True
    )

    viewfinder_resolution_dots: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Разрешение EVF в точках

    viewfinder_magnification: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Увеличение видоискателя

    viewfinder_coverage_percent: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Покрытие кадра, %


    # Экран
    screen_size_inches: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Диагональ экрана в дюймах

    screen_resolution_dots: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Разрешение экрана в точках

    screen_type: Mapped[ScreenType | None] = mapped_column(
        Enum(ScreenType, name='screen_type_enum'), nullable=True
    )

    is_touchscreen: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Сенсорный экран


    # Видео
    video_max_resolution: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Макс. разрешение видео ("8K", "4K", "1080p")

    video_max_fps_at_max_resolution: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Макс. fps на максимальном разрешении (30, 60, 120)

    video_max_bitrate_mbps: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Максимальный битрейт, Мбит/с

    has_log_profile: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Поддержка Log-профилей (S-Log, C-Log, N-Log)

    has_raw_video: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Внутренняя запись RAW-видео (ProRes RAW и т.п.)


    # === Хранение данных ===
    card_slots: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Количество слотов для карт памяти

    card_types: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Типы карт ("CFexpress Type B + SD UHS-II")
    # Можно сделать M2M-таблицу для строгой фильтрации


    # === Интерфейсы и связь ===
    has_wifi: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_bluetooth: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_gps: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    usb_type: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # Тип USB ("USB-C 3.2 Gen 2")

    has_headphone_jack: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Разъём для наушников (важно для видеографов)

    has_microphone_jack: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Микрофонный вход

    hdmi_type: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Тип HDMI ("Type A", "Micro Type D")


    # === Питание ===
    battery_model: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # Модель аккумулятора (EN-EL15c, LP-E6NH)

    battery_life_shots_cipa: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Количество кадров по стандарту CIPA

    has_usb_charging: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Зарядка по USB


    # === Корпус ===
    weight_g: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Вес с батареей и картой, грамм

    width_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    height_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    depth_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Габариты Ш×В×Г — если их нет в CameraPhysicalSpecMixin

    is_weather_sealed: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Пыле-/влагозащита

    has_built_in_flash: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Встроенная вспышка
