import math

from loguru import logger


def get_focal(focal, tc=None):
    if tc is None:
        return focal
    return focal * tc


def get_degrees_fov(sensor, focal):
    fov_w = math.degrees(2 * math.atan(sensor.width / (2 * focal)))
    fov_h = math.degrees(2 * math.atan(sensor.height / (2 * focal)))
    return fov_w, fov_h


def get_size_of_frame_on_plane(d, fov):
    return 2 * d * math.tan(fov / 2)


def calculate_fov(sensor, focal, distance, selected_tc):
    """Высчитывает высоту и ширину кадра на заданном расстоянии."""
    logger.debug('selected_tc="{}"',selected_tc)

    focal = get_focal(focal, selected_tc)
    fov_w, fov_h = get_degrees_fov(sensor, focal)

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
