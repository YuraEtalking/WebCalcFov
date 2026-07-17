import pytest
from pydantic import ValidationError

from backend.schemas.fov import FovCalcInput


def valid_data(**overrides):
    data = {
        'camera_id': 1,
        'lens_id': 2,
        'distance': 100,
        'focal': 50.0,
        'teleconverter_id': 3,
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize('value', [None, ''])
def test_teleconverter_empty_value_becomes_none(value):
    model = FovCalcInput(**valid_data(teleconverter_id=value))

    assert model.teleconverter_id is None


@pytest.mark.parametrize(
    ('raw_value', 'expected'),
    [
        (1, 1),
        ('2', 2),
        (' 3 ', 3),
    ],
)
def test_teleconverter_converts_value_to_int(raw_value, expected):
    model = FovCalcInput(**valid_data(teleconverter_id=raw_value))

    assert model.teleconverter_id == expected


@pytest.mark.parametrize('value', ['abc', '1.5', [], {}])
def test_teleconverter_rejects_invalid_value(value):
    with pytest.raises(ValidationError, match='Некорректное значение телеконвертера'):
        FovCalcInput(**valid_data(teleconverter_id=value))


@pytest.mark.parametrize(
    ('raw_value', 'expected'),
    [
        (1, 1),
        ('100', 100),
        (' 250 ', 250),
    ],
)
def test_distance_converts_to_int(raw_value, expected):
    model = FovCalcInput(**valid_data(distance=raw_value))

    assert model.distance == expected


@pytest.mark.parametrize('value', [0, -1, '-10'])
def test_distance_rejects_non_positive_values(value):
    with pytest.raises(ValidationError, match='Дистанция должна быть больше 0'):
        FovCalcInput(**valid_data(distance=value))


@pytest.mark.parametrize('value', ['abc', None, [], {}])
def test_distance_rejects_non_integer_values(value):
    with pytest.raises(ValidationError, match='Дистанция должна быть целым числом'):
        FovCalcInput(**valid_data(distance=value))


@pytest.mark.parametrize('value', [0.0, -1.0, -50.5])
def test_focal_rejects_non_positive_float_values(value):
    with pytest.raises(
        ValidationError,
        match='Фокусное не может быть равно или меньше ноля',
    ):
        FovCalcInput(**valid_data(focal=value))