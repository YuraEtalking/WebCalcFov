import piexif


def format_fraction(value):
    if isinstance(value, tuple) and len(value) == 2:
        num, den = value
        if den == 0:
            return None
        if num == 0:
            return '0'
        if den == 1:
            return str(num)
        return f'{num}/{den}'
    return str(value)

def decode_bytes(value):
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8', errors='ignore').strip('\x00')
        except Exception:
            return value
    return value

def rational_to_float(value):
    if isinstance(value, tuple) and len(value) == 2:
        num, den = value
        if den == 0:
            return None
        return num / den
    return value

def format_exif_value(tag_name, value):
    value = decode_bytes(value)

    if tag_name == 'ExposureTime':
        return format_fraction(value)

    if tag_name == 'FNumber':
        f = rational_to_float(value)
        return f'f/{f:.1f}' if f is not None else value

    if tag_name == 'FocalLength':
        f = rational_to_float(value)
        return f'{f:.0f} mm' if f is not None else value

def get_exif(img):
    exif_bytes = img.info.get('exif')
    if not exif_bytes:
        return {}

    exif_dict = piexif.load(exif_bytes)

    def get(tag_group, tag_name):
        for tag_id, meta in piexif.TAGS[tag_group].items():
            if meta['name'] == tag_name:
                return exif_dict[tag_group].get(tag_id)
        return None

    params = {
        'camera_model_name': decode_bytes(get('0th', 'Model')),
        'shutter_speed': format_exif_value(
            'ExposureTime',
            get('Exif', 'ExposureTime')
        ),
        'aperture': format_exif_value(
            'FNumber',
            get('Exif', 'FNumber')
        ),
        'iso': get('Exif', 'ISOSpeedRatings'),
        'focal_length': format_exif_value(
            'FocalLength',
            get('Exif', 'FocalLength')
        ),
        'lens_model_name': decode_bytes(get('Exif', 'LensModel')),
        'photographer_name': decode_bytes(get('0th', 'Artist')),
    }
    return params