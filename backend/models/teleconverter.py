from typing import TYPE_CHECKING

from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
)
from backend.models.enums import ConstructionType

if TYPE_CHECKING:
    from .lens import Lens
    from .associative_model import lens_teleconverter


class Teleconverter(
    IdMixin,
    ActiveMixin,
    Base,
    BayonetMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
):
    lenses: Mapped[list['Lens']] = relationship(
        secondary='lens_teleconverter',
        back_populates='teleconverters',
    )

    multiplier: Mapped[float] = mapped_column(Float)

    def __str__(self):
        return self.name
