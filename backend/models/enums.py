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


class FilterMountType(str, enum.Enum):
    """Тип крепления фильтра."""
    SCREW_IN = 'Резьбовой'
    DROP_IN = 'Вставной'
    REAR_GEL = 'Крепление для пленочного фильтра'
    NONE = 'Без крепления'


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
    THERMAL_LENS = 'Объектив для тепловизора'


class TypeDiaphragm(str, enum.Enum):
    ELECTRONIC = 'Электронная'
    MECHANICAL = 'Механическая'
    MANUAL = 'Ручная'
    CAMERA_CONTROLLED = 'camera-controlled'


class SensorFormat(str, enum.Enum):
    NON_STANDARD = 'NON_STANDARD'
    FULL_FRAME = 'Full Frame'
    APS_C = 'APS-C'
    MICRO_4_3 = '4/3'
    MEDIUM_FORMAT = 'medium_format'
    VOX_1280_12 = 'Thermal sensor VOx1280×1024:12μm'
    VOX_640_12 = 'Thermal sensor VOx640×512:12μm'
    VOX_384_12 = 'Thermal sensor VOx384×288:12μm'
    VOX_640_17 = 'Thermal sensor VOx640×512:17μm'
    VOX_384_17 = 'Thermal sensor VOx384×288:17μm'


SENSOR_FORMAT_SIZES = {
    SensorFormat.FULL_FRAME: (36.0, 24.0),
    SensorFormat.APS_C: (23.5, 15.6),
    SensorFormat.MICRO_4_3: (17.3, 13.0),
    SensorFormat.MEDIUM_FORMAT: (43.8, 32.9),
    SensorFormat.VOX_1280_12: (15.36, 12.3),
    SensorFormat.VOX_640_12: (7.7, 6.1),
    SensorFormat.VOX_384_12: (4.6, 3.5),
    SensorFormat.VOX_640_17: (10.9, 8.7),
    SensorFormat.VOX_384_17: (6.5, 4.9),
}

