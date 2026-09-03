from sqlalchemy import create_engine
from starlette_admin.contrib.sqla import Admin

from backend.core.config import settings
from .camera_lens import CameraLensAdmin
from .camera.camera import CameraAdmin
from .lens.lens import LensAdmin
from .lens.lens_spec import SpecLensAdmin
from .camera.camera_spec import SpecCameraAdmin
from .teleconverter import TeleconverterAdmin
from .link import LinkAdmin
from .image import ImageAdmin, LensImageLinkAdmin

from backend.models import (
    Camera, Lens, CameraLens,
    Teleconverter, Link, SpecLens, SpecCamera, Image, LensImageLink
)

sync_engine = create_engine(settings.database_sync_url)


def setup_admin(app):
    admin = Admin(
        engine=sync_engine,
        title='Админка',
        base_url='/admin',
        # templates_dir='templates/admin'
    )
    admin.add_view(CameraAdmin(Camera, icon='fa fa-camera'))
    admin.add_view(LensAdmin(Lens, icon='fa fa-less-than'))
    admin.add_view(CameraLensAdmin(CameraLens, icon='fa fa-camera-rotate'))
    admin.add_view(TeleconverterAdmin(Teleconverter, icon='fa fa-less-than'))
    admin.add_view(LinkAdmin(Link, icon='fa fa-link'))
    admin.add_view(SpecLensAdmin(SpecLens, icon='fa fa-list'))
    admin.add_view(SpecCameraAdmin(SpecCamera, icon='fa fa-list'))
    admin.add_view(ImageAdmin(Image, icon='fa fa-list'))
    admin.add_view(LensImageLinkAdmin(LensImageLink, icon='fa fa-list'))
    admin.mount_to(app)

