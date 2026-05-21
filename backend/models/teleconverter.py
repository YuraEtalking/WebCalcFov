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
    from .link import Link


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

    links: Mapped[list['Link']] = relationship(
        secondary='link_teleconverter',
        back_populates='teleconverters',
        order_by='Link.created_at',
    )

    multiplier: Mapped[float] = mapped_column(Float)

    def __str__(self):
        return self.name
