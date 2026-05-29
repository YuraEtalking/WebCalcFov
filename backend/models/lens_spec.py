from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
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


if TYPE_CHECKING:
    from .lens import Lens



class SpecLens(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    Base,
    TimeFieldsMixin,
    NameFieldsMixin
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

    diameter: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_aperture: Mapped[float | None] = mapped_column(Float, nullable=True)
    # compatible_format: todo нужно подумать просто перечисление форматов или связать с модель сенсоров(но зачем?)

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
    def angle_of_view_tele_ff_display(self) -> str:
        value = self.angle_of_view_tele_ff

        if value is None:
            return ''

        fov_w, fov_h = value
        return f'{fov_w:.1f}° × {fov_h:.1f}°'
