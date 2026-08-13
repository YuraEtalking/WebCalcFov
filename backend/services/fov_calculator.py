import math

from loguru import logger

from backend.models.sensor import Sensor


def get_focal(focal: float, tc: float | None) -> float:
    """Возвращает фокусное расстояние с учётом коэффициента телеконвертера."""
    if tc is None:
        return focal
    return focal * tc


def get_degrees_fov(
        width: float | None,
        height: float | None,
        focal: float
) -> tuple[float, float]:
    """Рассчитывает горизонтальный и вертикальный угол обзора в градусах."""
    if width is None or height is None:
        # По умолчанию Full Frame
        width, height = 36.0,  24.0

    fov_w = math.degrees(2 * math.atan(width / (2 * focal)))
    fov_h = math.degrees(2 * math.atan(height / (2 * focal)))
    return fov_w, fov_h


def get_size_of_frame_on_plane(d: int, fov: float) -> float:
    """Рассчитывает размер кадра на плоскости на заданном расстоянии."""
    return 2 * d * math.tan(fov / 2)


def calculate_fov(
        sensor: Sensor,
        focal: float,
        distance: int,
        selected_tc: float | None,
) -> dict[str, float]:
    """Высчитывает высоту и ширину кадра на заданном расстоянии."""
    # logger.debug('selected_tc="{}"', selected_tc)

    focal = get_focal(focal, selected_tc)
    fov_w, fov_h = get_degrees_fov(
        width=sensor.width,
        height=sensor.height,
        focal=focal
    )

    return {
        'focal': focal, 'tc': selected_tc,
        'fov_width_deg': fov_w,
        'fov_height_deg': fov_h,
        'frame_width_m': get_size_of_frame_on_plane(
            distance,
            math.radians(fov_w)
        ),
        'frame_height_m': get_size_of_frame_on_plane(
            distance,
            math.radians(fov_h)
        ),
    }
