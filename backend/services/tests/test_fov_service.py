from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from backend.core.constants.message_constants import (
    WARNING_CAMERA_AND_LENS_INCOMPATIBILITY,
)
from backend.services.fov_service import (
    EntityNotFoundError,
    FovServiceError,
    InvalidFovInputError,
    check_camera_and_lens_compatibility,
    checking_distance_within_range,
    get_lens_data,
    get_list_teleconverters,
    prepare_fov_response_data,
)


def make_teleconverter(tc_id: int, multiplier: float):
    return SimpleNamespace(id=tc_id, multiplier=multiplier)


def make_camera_lens(lens_id: int):
    return SimpleNamespace(lens_id=lens_id)


def make_lens():
    return SimpleNamespace(
        id=10,
        focal_wide=24,
        focal_tele=70,
        teleconverters=[
            make_teleconverter(1, 1.4),
            make_teleconverter(2, 1.4),
            make_teleconverter(3, 2.0),
        ],
    )


def make_camera(compatible_lens_ids: list[int] | None = None):
    compatible_lens_ids = compatible_lens_ids or [10]

    sensor = SimpleNamespace(id=1, width=36.0, height=24.0)
    return SimpleNamespace(
        id=20,
        sensor=sensor,
        camera_lenses=[
            make_camera_lens(lens_id)
            for lens_id in compatible_lens_ids
        ],
        compatible_lenses=[SimpleNamespace(id=lens_id) for lens_id in compatible_lens_ids],
    )


def make_input(
    lens_id: int = 10,
    camera_id: int = 20,
    focal: float | None = 50,
    distance: float = 10,
    teleconverter_id: int | None = None,
):
    return SimpleNamespace(
        lens_id=lens_id,
        camera_id=camera_id,
        focal=focal,
        distance=distance,
        teleconverter_id=teleconverter_id,
    )


def test_get_list_teleconverters_returns_unique_multipliers() -> None:
    teleconverters = [
        make_teleconverter(1, 1.4),
        make_teleconverter(2, 1.4),
        make_teleconverter(3, 2.0),
    ]

    result = get_list_teleconverters(teleconverters)

    assert result == [
        {'multiplier': 1.4, 'teleconverter_id': 1},
        {'multiplier': 2.0, 'teleconverter_id': 3},
    ]


def test_get_list_teleconverters_returns_empty_list_for_empty_input() -> None:
    assert get_list_teleconverters([]) == []


def test_check_camera_and_lens_compatibility_returns_true_for_compatible_lens() -> None:
    camera_lenses = [make_camera_lens(1), make_camera_lens(10)]

    assert check_camera_and_lens_compatibility(10, camera_lenses) is True


def test_check_camera_and_lens_compatibility_returns_false_for_incompatible_lens() -> None:
    camera_lenses = [make_camera_lens(1), make_camera_lens(2)]

    assert check_camera_and_lens_compatibility(10, camera_lenses) is False


def test_checking_distance_within_range_uses_tele_focal_by_default() -> None:
    assert checking_distance_within_range(
        focal=None,
        focal_wide=24,
        focal_tele=70,
    ) == 70


@pytest.mark.parametrize('focal', [24, 50, 70])
def test_checking_distance_within_range_accepts_boundaries_and_middle(
    focal: float,
) -> None:
    assert checking_distance_within_range(
        focal=focal,
        focal_wide=24,
        focal_tele=70,
    ) == focal


@pytest.mark.parametrize('focal', [23.9, 70.1])
def test_checking_distance_within_range_rejects_out_of_range_focal(
    focal: float,
) -> None:
    with pytest.raises(
        InvalidFovInputError,
        match='Фокусное выходит за диапазон объектива',
    ):
        checking_distance_within_range(
            focal=focal,
            focal_wide=24,
            focal_tele=70,
        )


@pytest.mark.asyncio
async def test_prepare_fov_response_data_raises_when_lens_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_lens_mock = AsyncMock(return_value=None)
    get_camera_mock = AsyncMock()

    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        get_lens_mock,
    )
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_camera_with_sensor',
        get_camera_mock,
    )

    with pytest.raises(EntityNotFoundError, match='Объектив не выбран'):
        await prepare_fov_response_data(
            input_data=make_input(),
            session=AsyncMock(),
        )

    get_camera_mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_prepare_fov_response_data_raises_when_camera_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_lens_mock = AsyncMock(return_value=make_lens())
    get_camera_mock = AsyncMock(return_value=None)

    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        get_lens_mock,
    )
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_camera_with_sensor',
        get_camera_mock,
    )

    with pytest.raises(EntityNotFoundError, match='Камера не выбрана'):
        await prepare_fov_response_data(
            input_data=make_input(),
            session=AsyncMock(),
        )


@pytest.mark.asyncio
async def test_prepare_fov_response_data_returns_success_for_compatible_entities(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lens = make_lens()
    camera = make_camera(compatible_lens_ids=[10])
    input_data = make_input(focal=None, distance=15)

    calculate_mock = AsyncMock()
    # calculate_fov синхронная функция, поэтому заменяем обычной функцией.
    def calculate_fov_mock(**kwargs):
        return {'focal': 70, 'tc': None, 'frame_width_m': 10}

    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        AsyncMock(return_value=lens),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_camera_with_sensor',
        AsyncMock(return_value=camera),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.calculate_fov',
        calculate_fov_mock,
    )

    result = await prepare_fov_response_data(
        input_data=input_data,
        session=AsyncMock(),
    )

    assert result['data']['camera'] is camera
    assert result['data']['lens'] is lens
    assert result['data']['sensor'] is camera.sensor
    assert result['data']['distance'] == 15
    assert result['data']['lens_list'] == camera.compatible_lenses

    assert result['result'] == {
        'focal': 70,
        'tc': None,
        'frame_width_m': 10,
    }
    assert result['focal'] == 70
    assert result['teleconverter_id'] is None
    assert result['message'] == 'Расчёт выполнен'
    assert result['message_type'] == 'success'
    assert result['teleconverters'] == [
        {'multiplier': 1.4, 'teleconverter_id': 1},
        {'multiplier': 2.0, 'teleconverter_id': 3},
    ]


@pytest.mark.asyncio
async def test_prepare_fov_response_data_returns_warning_for_incompatible_lens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lens = make_lens()
    camera = make_camera(compatible_lens_ids=[999])

    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        AsyncMock(return_value=lens),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_camera_with_sensor',
        AsyncMock(return_value=camera),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.calculate_fov',
        lambda **kwargs: {'focal': 50},
    )

    result = await prepare_fov_response_data(
        input_data=make_input(focal=50),
        session=AsyncMock(),
    )

    assert result['message'] == WARNING_CAMERA_AND_LENS_INCOMPATIBILITY
    assert result['message_type'] == 'warning'


@pytest.mark.asyncio
async def test_prepare_fov_response_data_uses_selected_teleconverter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lens = make_lens()
    camera = make_camera()
    captured_arguments = {}

    def calculate_fov_mock(**kwargs):
        captured_arguments.update(kwargs)
        return {'focal': 70, 'tc': 1.4}

    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        AsyncMock(return_value=lens),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_camera_with_sensor',
        AsyncMock(return_value=camera),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.calculate_fov',
        calculate_fov_mock,
    )

    result = await prepare_fov_response_data(
        input_data=make_input(focal=50, distance=10, teleconverter_id=1),
        session=AsyncMock(),
    )

    assert captured_arguments == {
        'sensor': camera.sensor,
        'focal': 50,
        'distance': 10,
        'selected_tc': 1.4,
    }
    assert result['teleconverter_id'] == 1


@pytest.mark.asyncio
async def test_prepare_fov_response_data_rejects_foreign_teleconverter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        AsyncMock(return_value=make_lens()),
    )
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_camera_with_sensor',
        AsyncMock(return_value=make_camera()),
    )

    with pytest.raises(
        FovServiceError,
        match='Выбранный телеконвертер не принадлежит объективу',
    ):
        await prepare_fov_response_data(
            input_data=make_input(teleconverter_id=999),
            session=AsyncMock(),
        )


@pytest.mark.asyncio
async def test_get_lens_data_returns_lens_default_focal_and_teleconverters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lens = make_lens()
    get_lens_mock = AsyncMock(return_value=lens)

    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        get_lens_mock,
    )

    session = AsyncMock()
    result = await get_lens_data(lens_id=10, session=session)

    get_lens_mock.assert_awaited_once_with(10, session)
    assert result == {
        'lens': lens,
        'focal': 70,
        'teleconverters': [
            {'multiplier': 1.4, 'teleconverter_id': 1},
            {'multiplier': 2.0, 'teleconverter_id': 3},
        ],
    }


@pytest.mark.asyncio
async def test_get_lens_data_raises_when_lens_not_found(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        'backend.services.fov_service.get_active_lens_with_teleconverters',
        AsyncMock(return_value=None),
    )

    with pytest.raises(EntityNotFoundError, match='Объектив не выбран'):
        await get_lens_data(lens_id=10, session=AsyncMock())