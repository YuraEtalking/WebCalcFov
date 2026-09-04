import math
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Enum,
    Integer,
    SmallInteger,
    String,
    Text,
    event,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

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
    SensorTechnology,
    MediumType,
    ViewfinderType,
    ScreenType,
    CardType,
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



    # === Тип камеры ===
    camera_category: Mapped[CameraCategory | None] = mapped_column(
        Enum(CameraCategory, name='camera_category_enum'),
        nullable=True,
    )

    camera_type: Mapped[CameraType | None] = mapped_column(
        Enum(CameraType, name='camera_type_enum'),
        nullable=True,
    )

    medium_type: Mapped[MediumType | None] = mapped_column(
        Enum(MediumType, name='medium_type_enum'),
        nullable=True,
    )



    # === Процессор ===
    processor: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )



    # === Сенсор ===
    sensor_format: Mapped[SensorFormat | None] = mapped_column(
        Enum(SensorFormat, name='sensor_format_enum'),
        nullable=True,
    )

    sensor_technology: Mapped[SensorTechnology | None] = mapped_column(
        Enum(SensorTechnology, name='sensor_technology_enum'),
        nullable=True,
    )

    has_global_shutter: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )

    max_raw_bit_depth: Mapped[int | None] = mapped_column(
        SmallInteger,nullable=True
    )

    max_readout_time_ms: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )

    sensor_width_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    sensor_height_mm: Mapped[float | None] = mapped_column(Float, nullable=True)

    sensor_pixels_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sensor_pixels_height: Mapped[int | None] = mapped_column(Integer, nullable=True)

    effective_megapixels: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    native_aspect_ratio: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    pixel_pitch_um: Mapped[float | None] = mapped_column(Float, nullable=True)


    @property
    def crop_factor(self) -> float | None:
        if self.sensor_width_mm and self.sensor_height_mm:
            diagonal = math.sqrt(
                self.sensor_width_mm ** 2 + self.sensor_height_mm ** 2
            )
            return round(FULL_FRAME_DIAGONAL / diagonal, 1)
        return None



    # === Стабилизация ===
    has_ibis: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    ibis_stops: Mapped[float | None] = mapped_column(Float, nullable=True)



    # === ISO ===
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



    # === Затвор ===
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



    # === Серийная съёмка ===
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



    # === Буфер ===
    buffer_high_efficiency_raw_jpg_frames: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Высокоэффективное сжатие RAW + JPG

    buffer_lossless_compressed_raw_frames: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Без сжатия RAW

    buffer_high_efficiency_raw_frames: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Высокоэффективное сжатие RAW



    # === Автофокус ===
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



    # === Видоискатель ===
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



    # === Экран ===
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



    # === Видео RAW ===
    raw_video_max_resolution: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # Макс. разрешение RAW видео

    raw_video_max_fps_at_max_resolution: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Макс. fps на максимальном разрешении RAW

    raw_video_max_fps: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # RAW видео макс. fps

    raw_video_max_resolution_at_max_fps: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # Макс. разрешение RAW при макс. fps

    raw_video_max_bitrate_mbps: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Максимальный битрейт RAW видео, Мбит/с

    @property
    def raw_video_max_rate_mb_s(self) -> float | None:
        """Максимальная скорость потока RAW-видео, МБ/с."""
        if self.raw_video_max_bitrate_mbps is None:
            return None

        return self.raw_video_max_bitrate_mbps / 8

    raw_video_max_bit_depth: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Максимальная битность RAW видео

    has_internal_raw_video: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Внутренняя RAW-запись

    has_external_raw_video: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # RAW через HDMI / SDI на внешний рекордер



    # === Видео кодеки ===
    has_log_profile: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )  # Поддержка Log-профилей (S-Log, C-Log, N-Log)

    video_codecs: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )  # поддерживаемые кодеки

    video_max_bit_depth: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Максимальная битность RAW видео

    video_max_bitrate_mbps: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Максимальный битрейт, Мбит/с

    @property
    def video_max_rate_mb_s(self) -> float | None:
        """Максимальная скорость потока, МБ/с."""
        if self.raw_video_max_bitrate_mbps is None:
            return None

        return self.raw_video_max_bitrate_mbps / 8




    # === Хранение данных ===
    card_slots: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Количество слотов для карт памяти

    card_types: Mapped[list[CardType] | None] = mapped_column(
        ARRAY(
            Enum(
                CardType,
                name='card_type_enum',
                native_enum=True,
            )
        ),
        nullable=True,
        comment='Поддерживаемые типы карт памяти',
    )



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



    # === Встроенная вспышка ===
    has_built_in_flash: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )



    # === Питание ===
    battery_model: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    battery_life_shots_cipa: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # Количество кадров по стандарту CIPA

    has_usb_charging: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )

    battery_grip: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    ac_adapter: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Зарядное устройство.



    # === Пыле-/влагозащита ===
    is_weather_sealed: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True
    )
    operating_environment: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # температуры среды



    # === Штативное крепление ===
    tripod_socket: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )



    # === Комплект поставки ===
    supplied_accessories: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

@event.listens_for(SpecCamera, 'before_insert')
@event.listens_for(SpecCamera, 'before_update')
def compute_pixel_pitch(mapper, connection, target):
    """Высчитывает размер пикселя для поля pixel_pitch_um."""
    if (
            target.sensor_width_mm is not None
            and target.sensor_pixels_width is not None
            and target.sensor_width_mm > 0
            and target.sensor_pixels_width > 0
    ):
        target.pixel_pitch_um = round(
            target.sensor_width_mm / target.sensor_pixels_width * 1000, 2
        )
    else:
        target.pixel_pitch_um = None
