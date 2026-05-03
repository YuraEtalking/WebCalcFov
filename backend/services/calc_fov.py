import math

from loguru import logger

from backend.core.constants import PI


def get_focal(focal, tc=None):
    if tc is None:
        tc = 1.0
    return focal * tc


def get_degrees_fov(sensor, focal):
    fov_w = math.degrees(2 * math.atan(sensor.width / (2 * focal)))
    fov_h = math.degrees(2 * math.atan(sensor.height / (2 * focal)))
    return fov_w, fov_h


def calc(sensor, lens, radius):
    """Высчитывает высоту и ширину кадра на заданном расстоянии."""

    meters_per_degree = ((radius * 2) * PI) / 360
    focal = get_focal(lens.focal_max)
    fov_w, fov_h = get_degrees_fov(sensor, focal)

    data_tc = []
    if lens.teleconverters:
        for tc in lens.teleconverters:
            focal = get_focal(lens.focal_max, tc.multiplier)
            tc_fov_w, tc_fov_h = get_degrees_fov(sensor, focal)

            data_tc.append({
                'name': tc.multiplier,
                'focal':focal,
                'width': f'{meters_per_degree * tc_fov_w:.1f} м., {tc_fov_w:.1f}°',
                'height': f'{meters_per_degree * tc_fov_h:.1f} м., {tc_fov_h:.1f}°',
            })


    return {
        'focal': lens.focal_max,
        'width': f'{meters_per_degree * fov_w:.1f} м., {fov_w:.1f}°',
        'height': f'{meters_per_degree * fov_h:.1f} м., {fov_h:.1f}°',
        'with_teleconverter': data_tc,
    }
