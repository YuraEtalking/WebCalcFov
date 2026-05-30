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
from backend.models.enums import ConstructionType, LensType


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

    # Формата покрытия матрицы todo переделать на Enum
    coverage_format: Mapped[str | None] = mapped_column(String, nullable=True)


    # Диафрагма
    min_aperture: Mapped[float | None] = mapped_column(Float, nullable=True)
    aperture_blades: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type_diaphragm: Mapped[int | None] = mapped_column(Integer, nullable=True) # todo переделать str или Enum
    aperture_blades_rounded: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Фильтры
    filter_size_mm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    supports_front_filters: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    rear_filter_holder: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    filter_mount_type: Mapped[str | None] = mapped_column(String, nullable=True) # screw-in, drop-in, rear gel, none

    # Фокусировка
    focus_type: Mapped[str | None] = mapped_column(String, nullable=True)
    autofocus: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    full_time_manual_focus: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    min_focus_distance_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    autofocus_motor_type: Mapped[str | None] = mapped_column(String, nullable=True)

    # Стабилизация
    image_stabilization: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    stabilization_name: Mapped[str | None] = mapped_column(String, nullable=True)
    stabilization_stops: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Зум
    zoom_type: Mapped[str | None] = mapped_column(String, nullable=True)
    internal_zoom: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    zoom_lock: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Бленда и аксессуары
    hood_model: Mapped[str | None] = mapped_column(String, nullable=True)
    hood_included: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tripod_collar_included: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tripod_collar_removable: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    case_included: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Макро-возможности
    is_macro: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    working_distance_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    maximum_magnification_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    reproduction_ratio_text: Mapped[str | None] = mapped_column(String, nullable=True)

    # Комплект поставки
    supplied_accessories: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Дополнительно
    weather_sealing: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    dust_moisture_resistant: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    fluorine_coating: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    # Конструкция объектива
    lens_construction: Mapped[str | None] = mapped_column(Text, nullable=True)


    @property
    def angle_of_view_wide_ff(self) -> tuple[float, float] | None:
        """
        Горизонтальный и вертикальный угол обзора для широкого угла.

        Рассчитывается для Full Frame.
        """
        if self.lens is None or self.lens.focal_wide is None:
            return None

        return get_degrees_fov(sensor=None, focal=self.lens.focal_wide)


    @property
    def angle_of_view_tele_ff(self) -> tuple[float, float] | None:
        """
        Горизонтальный и вертикальный угол обзора для теле положения.

        Рассчитывается для Full Frame.
        """
        if self.lens is None or self.lens.focal_tele is None:
            return None

        return get_degrees_fov(sensor=None, focal=self.lens.focal_tele)

    @property
    def angle_of_view_wide_ff_display(self) -> str:
        value = self.angle_of_view_wide_ff

        if value is None:
            return ''

        fov_w, fov_h = value
        return f'{fov_w:.1f}° × {fov_h:.1f}°'

    @property
    def angle_of_view_tele_ff_display(self) -> str:
        value = self.angle_of_view_tele_ff

        if value is None:
            return ''

        fov_w, fov_h = value
        return f'{fov_w:.1f}° × {fov_h:.1f}°'

    @property
    def construction_type(self):
        if self.lens is None:
            return None

        if self.lens.focal_wide != self.lens.focal_tele:
            return ConstructionType.ZOOM.value
        return ConstructionType.PRIME.value