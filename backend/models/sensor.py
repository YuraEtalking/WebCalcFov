from sqlalchemy import Column, Integer

from backend.core.db import Base
from backend.models.mixins import (
    ActiveMixin,
    CommonFieldsMixin,
    TimeFieldsMixin,
)


class Sensor(ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin):
    width = Column(Integer)
    height = Column(Integer)
    crop = Column(Integer)