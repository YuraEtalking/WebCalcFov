import math

def calc(sensor, lens, dist):

    fov_w = math.degrees(2 * math.atan(sensor.width / (2 * lens.focal_max)))
    fov_h = math.degrees(2 * math.atan(sensor.height / (2 * lens.focal_max)))

    radius = dist * 2
    pi = float(radius * 3.14159)
    grad = float(pi / 360)
    result_w = float(grad * fov_w)
    result_h = float(grad * fov_h)
    return {
        'width': f'{result_w:.1f} м, {fov_w:.1f}°',
        'height': f'{result_h:.1f} м, {fov_h:.1f}°',
    }
