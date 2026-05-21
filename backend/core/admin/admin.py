from sqlalchemy import create_engine
from sqladmin import Admin, ModelView

from backend.core.config import settings
from .camera_lens import CameraLensAdmin
from .camera import CameraAdmin
from .lens import LensAdmin
from .sensor import SensorAdmin
from .teleconverter import TeleconverterAdmin
from .link import LinkAdmin


sync_engine = create_engine(settings.database_sync_url)

def setup_admin(app):
    admin = Admin(app, sync_engine)
    admin.add_view(CameraAdmin)
    admin.add_view(LensAdmin)
    admin.add_view(SensorAdmin)
    admin.add_view(CameraLensAdmin)
    admin.add_view(TeleconverterAdmin)
    admin.add_view(LinkAdmin)