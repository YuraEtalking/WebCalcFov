import math

import pytest

from backend.models.sensor import Sensor
from backend.services.fov_calculator import (
    calculate_fov,
    get_degrees_fov,
    get_focal,
    get_size_of_frame_on_plane,
)


@pytest.mark.parametrize(
    ('focal', 'tc', 'expected'),
    [
        (50.0, None, 50.0),
        (50.0, 1.4, 70.0),
        (100.0, 2.0, 200.0),
    ],
)
def test_get_focal(
    focal: float,
    tc: float | None,
    expected: float,
) -> None:
    assert get_focal(focal, tc) == pytest.approx(expected)


def test_get_degrees_fov_with_sensor_dimensions() -> None:
    fov_width, fov_height = get_degrees_fov(
        width=36.0,
        height=24.0,
        focal=50.0,
    )

    assert fov_width == pytest.approx(39.5978, abs=0.0001)
    assert fov_height == pytest.approx(26.9915, abs=0.0001)


@pytest.mark.parametrize(
    ('width', 'height'),
    [
        (None, None),
        (None, 24.0),
        (36.0, None),
    ],
)
def test_get_degrees_fov_uses_full_frame_by_default(
    width: float | None,
    height: float | None,
) -> None:
    actual_width, actual_height = get_degrees_fov(
        width=width,
        height=height,
        focal=50.0,
    )
    expected_width, expected_height = get_degrees_fov(
        width=36.0,
        height=24.0,
        focal=50.0,
    )

    assert actual_width == pytest.approx(expected_width)
    assert actual_height == pytest.approx(expected_height)


def test_get_size_of_frame_on_plane() -> None:
    result = get_size_of_frame_on_plane(
        d=10,
        fov=math.radians(90),
    )

    assert result == pytest.approx(20.0)


def test_calculate_fov_with_teleconverter(sensor: Sensor) -> None:
    result = calculate_fov(
        sensor=sensor,
        focal=50.0,
        distance=10,
        selected_tc=1.4,
    )

    expected_fov_width, expected_fov_height = get_degrees_fov(
        width=sensor.width,
        height=sensor.height,
        focal=70.0,
    )

    assert result['focal'] == pytest.approx(70.0)
    assert result['tc'] == pytest.approx(1.4)
    assert result['fov_width_deg'] == pytest.approx(expected_fov_width)
    assert result['fov_height_deg'] == pytest.approx(expected_fov_height)

    assert result['frame_width_m'] == pytest.approx(
        get_size_of_frame_on_plane(
            d=10,
            fov=math.radians(expected_fov_width),
        )
    )
    assert result['frame_height_m'] == pytest.approx(
        get_size_of_frame_on_plane(
            d=10,
            fov=math.radians(expected_fov_height),
        )
    )


def test_calculate_fov_without_teleconverter(sensor: Sensor) -> None:
    result = calculate_fov(
        sensor=sensor,
        focal=50.0,
        distance=10,
        selected_tc=None,
    )

    assert result['focal'] == pytest.approx(50.0)
    assert result['tc'] is None