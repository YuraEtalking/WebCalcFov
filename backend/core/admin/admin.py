from sqlalchemy import create_engine
from starlette_admin.contrib.sqla import Admin

from backend.core.config import settings
from .camera_lens import CameraLensAdmin
from .camera import CameraAdmin
from .lens import LensAdmin
from .lens_spec import SpecLensAdmin
from .sensor import SensorAdmin
from .teleconverter import TeleconverterAdmin
from .link import LinkAdmin

from backend.models import (
    Camera, Lens, Sensor, CameraLens,
    Teleconverter, Link, SpecLens,
)

sync_engine = create_engine(settings.database_sync_url)


def setup_admin(app):
    admin = Admin(
        engine=sync_engine,
        title='Админка',
        base_url='/admin',
    )
    admin.add_view(CameraAdmin(Camera, icon='fa fa-camera'))
    admin.add_view(LensAdmin(Lens, icon='fa fa-less-than'))
    admin.add_view(SensorAdmin(Sensor, icon='fa fa-microchip'))
    admin.add_view(CameraLensAdmin(CameraLens, icon='fa fa-camera-rotate'))
    admin.add_view(TeleconverterAdmin(Teleconverter, icon='fa fa-less-than'))
    admin.add_view(LinkAdmin(Link, icon='fa fa-link'))
    admin.add_view(SpecLensAdmin(SpecLens, icon='fa fa-list'))
    admin.mount_to(app)

