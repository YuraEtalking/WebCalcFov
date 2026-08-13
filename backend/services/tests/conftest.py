import pytest

from backend.models.sensor import Sensor
from backend.models.enums import SensorFormat


@pytest.fixture
def sensor() -> Sensor:
    return Sensor(
        width=36.0,
        height=24.0,
        sensor_format=SensorFormat.FULL_FRAME,
    )