from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.models.image import Image


def images_by_role(entity, role: str) -> list['Image']:
    """Собирает изображения объекта с указанной ролью."""
    return [
        link.image
        for link in entity.image_links
        if link.role == role and link.image is not None
    ]