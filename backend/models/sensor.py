from sqlalchemy import Column, Integer

from backend.core import ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin


class Sensor(ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin):
    width = Column(Integer, gt=1)
    height = Column(Integer, gt=1)
    crop = Column(Integer, gt=1)