from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.constants import WARNING_CAMERA_AND_LENS_INCOMPATIBILITY
from backend.crud.camera import get_active_camera_with_sensor
from backend.crud.lens import get_active_lens_with_teleconverters
from backend.schemas.fov import FovCalcInput
from backend.services.calc_fov import calculate_fov


class FovServiceError(Exception):
    pass


class EntityNotFoundError(FovServiceError):
    pass


class ValidationError(FovServiceError):
    pass


def get_list_teleconverters(lens_teleconverters):
    """Отдает список телеконверторов с уникальным multiplier"""
    tc_list = []
    if lens_teleconverters:
        for tc in lens_teleconverters:
            if not any(tc.multiplier == i['multiplier'] for i in tc_list):
                tc_list.append({
                    'multiplier': tc.multiplier,
                    'teleconverter_id': tc.id,
                })

    return tc_list


def check_camera_and_lens_compatibility(lens_id, camera_lenses):
    """Проверяет совместимость камеры и объектива."""
    return any(cl.lens_id == lens_id for cl in camera_lenses)


async def prepare_fov_response_data(
        input_data: FovCalcInput,
        session: AsyncSession
):
    """Подготавливает данные для ответа."""
    distance = input_data.distance

    lens = await get_active_lens_with_teleconverters(input_data.lens_id, session)
    if not lens:
        raise EntityNotFoundError('Объектив не выбран')

    camera = await get_active_camera_with_sensor(input_data.camera_id, session)
    if not camera:
        raise EntityNotFoundError('Камера не выбрана')

    message = 'Расчёт выполнен'
    message_type = 'success'

    if not check_camera_and_lens_compatibility(
            lens_id=input_data.lens_id,
            camera_lenses=camera.camera_lenses,
    ):
        message = WARNING_CAMERA_AND_LENS_INCOMPATIBILITY
        message_type = 'warning'

    focal = input_data.focal or lens.focal_max

    teleconverters = get_list_teleconverters(lens.teleconverters)

    teleconverter_id = input_data.teleconverter_id

    selected_tc = None
    if teleconverter_id is not None:
        selected_tc_obj = next(
            (tc for tc in lens.teleconverters if tc.id == teleconverter_id),
            None
        )
        if selected_tc_obj is None:
            raise FovServiceError(
                'Выбранный телеконвертер не принадлежит объективу')
        selected_tc = selected_tc_obj.multiplier

    result = calculate_fov(
        sensor=camera.sensor,
        focal=focal,
        distance=distance,
        selected_tc=selected_tc
    )
    return {
        'data': {
            'camera': camera,
            'lens': lens,
            'sensor': camera.sensor,
            'distance': distance,
        },
        'result': result,
        'focal': focal,
        'teleconverter_id': teleconverter_id,
        'teleconverters': teleconverters,
        'message': message,
        'message_type': message_type,
    }


async def get_lens_data(lens_id: int, session: AsyncSession):
    lens = await get_active_lens_with_teleconverters(lens_id, session)

    if not lens:
        raise EntityNotFoundError('Объектив не выбран')

    teleconverters = get_list_teleconverters(lens.teleconverters)

    return {
            'lens': lens,
            'focal': lens.focal_max,
            'teleconverters': teleconverters,
    }
