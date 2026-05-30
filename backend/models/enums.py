import enum


class BayonetType(str, enum.Enum):
    """Наименование байонета."""
    Z = 'Nikon Z'
    F = 'Nikon F'
    EF = 'Canon EF'
    EF_S = 'Canon EF-S'
    RF = 'Canon RF'
    EF_M = 'Canon EF-M'
    A = 'Sony A'
    E = 'Sony E'
    X = 'Fujifilm X-Mount'
    G = 'Fujifilm G-Mount'
    K = 'Pentax K'


class CompatibilityType(str, enum.Enum):
    """Тип соединения камеры и объектива."""
    DIRECT = 'прямое соединение'
    WITH_CONVERTOR = 'переходник'


class ConstructionType(str, enum.Enum):
    """Конструкция объектива."""
    ZOOM = 'Зум'
    PRIME = 'Фикс'

class LensType(str, enum.Enum):
    """Тип объектива."""
    MACRO = 'Макро'
    FISHEYE = 'Рыбий глаз'
    TILT_SHIFT = 'Смещение оси'
    SUPER_TELEPHOTO = 'Длиннофокусный'
    WIDE_ANGLE = 'Широкоугольный'
    STANDARD = 'Стандартный'
    PORTRAIT = 'Портретный'
    CINE = 'Кинообъектив'
    PANCAKE = 'Блинчик'


# FULL_FRAME = ('Full Frame', 36.0, 24.0)
# APS_C = ('APS-C', 23.6, 15.8)
# MICRO_4_3 = ('4/3', 17.3, 13.0)
# MEDIUM_FORMAT = ('medium_format', 43.8, 32.9)
#
# VOX_1280_12 = ('VOx1280×1024:12μm', 15.36, 12.3)
#
# VOX_640_12 = ('VOx640×512:12μm', 7.7, 6.1)
# VOX_384_12 = ('VOx384×288:12μm', 4.6, 3.5)
#
# VOX_640_17 = ('VOx640×512:17μm', 10.9, 8.7)
# VOX_384_17 = ('VOx384×288:17μm', 6.5, 4.9)