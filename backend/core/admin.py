from sqlalchemy import create_engine
from sqladmin import Admin, ModelView

from backend.core.config import settings
from backend.models.camera import Camera

sync_engine = create_engine(settings.database_sync_url)

class CameraAdmin(ModelView, model=Camera):
    column_list = [Camera.id, Camera.manufacturer, Camera.name, Camera.bayonet]

def setup_admin(app):
    admin = Admin(app, sync_engine)
    admin.add_view(CameraAdmin)