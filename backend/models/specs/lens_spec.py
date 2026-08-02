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
from backend.services.fov_calculator import get_degrees_fov
from backend.models.specs.spec_mixins import LensPhysicalSpecMixin
from backend.models.specs.utils import positive_checks
from backend.models.enums import (
    SensorFormat,
    ConstructionType,
    LensType,
    TypeDiaphragm,
    SENSOR_FORMAT_SIZES,
    FilterMountType,FocusType,AutofocusMotorType,ZoomType
)


if TYPE_CHECKING:
    from models.lens import Lens



class SpecLens(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    Base,
    TimeFieldsMixin,
    NameFieldsMixin,
    LensPhysicalSpecMixin
):
    """Модель спецификаций для объектива.

    Все поля характеристик должны быть nullable=True, объект SpecLens
    создается вместе с объектом Lens, так как ограничение админки не позволяет
    наполнить объект SpecLens данными сразу вместе с Lens."""

    __table_args__ = positive_checks(
        'speclens',
        'min_aperture',
        'aperture_blades',
        'filter_size_mm',
        'min_focus_distance_m',
        'stabilization_stops',
        'max_magnification',
    )

    lens_id: Mapped[int] = mapped_column(
        ForeignKey('lens.id'),
        unique=True,
        nullable=False,
    )
    lens: Mapped['Lens'] = relationship(back_populates='spec',)

    lens_type: Mapped[LensType] = mapped_column(
        Enum(LensType,
             name='lens_type_enum'),
        nullable=False,
        default=LensType.STANDARD,
    )

    # Формат покрытия матрицы
    coverage_format: Mapped[SensorFormat] = mapped_column(
        Enum(SensorFormat, name='coverage_format_enum'),
        nullable=False,
        default=SensorFormat.FULL_FRAME,
    )


    # Диафрагма
    min_aperture: Mapped[float | None] = mapped_column(Float, nullable=True)
    aperture_blades: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type_diaphragm: Mapped[TypeDiaphragm] = mapped_column(
        Enum(TypeDiaphragm, name='type_diaphragm_enum'),
        nullable=False,
        default=TypeDiaphragm.ELECTRONIC,
    )
    aperture_blades_rounded: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


    # Фильтры
    filter_size_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    supports_front_filters: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    rear_filter_holder: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    filter_mount_type: Mapped[FilterMountType] = mapped_column(
        Enum(FilterMountType, name='filter_mount_type_enum'),
        nullable=False,
        default=FilterMountType.SCREW_IN,
    )


    # Фокусировка
    focus_type: Mapped[FocusType] = mapped_column(
        Enum(FocusType, name='focus_type_enum'),
        nullable=False,
        default=FocusType.INTERNAL,
    )
    autofocus: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    full_time_manual_focus: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    min_focus_distance_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    autofocus_motor_type: Mapped[AutofocusMotorType] = mapped_column(
        Enum(AutofocusMotorType, name='autofocus_motor_type_enum'),
        nullable=False,
        default=AutofocusMotorType.OTHER,
    )
    brand_name_autofocus: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )


    # Стабилизация
    image_stabilization: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    stabilization_name: Mapped[str | None] = mapped_column(String, nullable=True)
    stabilization_stops: Mapped[float | None] = mapped_column(Float, nullable=True)


    # Зум
    zoom_type: Mapped[ZoomType] = mapped_column(
        Enum(ZoomType, name='zoom_type_enum'),
        nullable=False,
        default=ZoomType.NON_ZOOM,
    )
    internal_zoom: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    zoom_lock: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


    # Интегрированный телеконвертор
    is_tc_integrated: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


    # Макро-возможности
    is_macro: Mapped[bool | None] = mapped_column(Boolean,nullable=True)
    max_magnification: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )


    # Бленда и аксессуары
    hood_model: Mapped[str | None] = mapped_column(String, nullable=True)
    hood_included: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tripod_collar_included: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tripod_collar_removable: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    case_included: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


    # Комплект поставки
    supplied_accessories: Mapped[str | None] = mapped_column(Text, nullable=True)


    # Дополнительно
    weather_sealing: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    dust_moisture_resistant: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    fluorine_coating: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


    # Углы обзора объектива
    @property
    def angle_of_view_wide(self) -> str | None:
        """
        Горизонтальный и вертикальный угол обзора для широкого угла.

        Рассчитывается для Full Frame.
        """
        if self.lens is None or self.lens.focal_wide is None:
            return None

        sensor_format = SENSOR_FORMAT_SIZES.get(self.coverage_format, None)
        if sensor_format is None:
            return None
        width, height = sensor_format

        fov_w, fov_h = get_degrees_fov(
            width=width,
            height=height,
            focal=self.lens.focal_wide
        )
        return f'w: {fov_w:.1f}° × h: {fov_h:.1f}°'

    @property
    def angle_of_view_tele(self) -> str | None:
        """
        Горизонтальный и вертикальный угол обзора для теле положения.

        Рассчитывается для Full Frame.
        """
        if self.lens is None or self.lens.focal_tele is None:
            return None

        sensor_format = SENSOR_FORMAT_SIZES.get(self.coverage_format, None)
        if sensor_format is None:
            return None
        width, height = sensor_format

        fov_w, fov_h = get_degrees_fov(
            width=width,
            height=height,
            focal=self.lens.focal_tele
        )
        return f'w: {fov_w:.1f}° × h: {fov_h:.1f}°'


    # Конструкция объектива
    @property
    def construction_type(self):
        if self.lens is None:
            return None

        if self.lens.focal_wide != self.lens.focal_tele:
            return ConstructionType.ZOOM.value
        return ConstructionType.PRIME.value
