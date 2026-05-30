from typing import TYPE_CHECKING

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from starlette.requests import Request

from backend.core.db import Base
from backend.models.mixins import (
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    TimeFieldsMixin,
)


if TYPE_CHECKING:
    from .camera import Camera
    from .lens import Lens
    from .teleconverter import Teleconverter


class Link(
    IdMixin,
    ActiveMixin,
    AdminReprMixin,
    Base,
    TimeFieldsMixin,
):
    """Модель ссылок на обзоры/тесты/статьи."""

    __admin_repr_field__ = 'title'

    cameras: Mapped[list['Camera']] = relationship(
        secondary='link_camera',
        back_populates='links',
    )

    lenses: Mapped[list['Lens']] = relationship(
        secondary='link_lens',
        back_populates='links',
    )

    teleconverters: Mapped[list['Teleconverter']] = relationship(
        secondary='link_teleconverter',
        back_populates='links',
    )

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text(),
        nullable=False,
    )

    def __str__(self):
        return self.title
