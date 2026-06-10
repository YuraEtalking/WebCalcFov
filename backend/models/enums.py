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
    DIRECT = 'direct'  # Прямое соединение
    WITH_CONVERTOR = 'with_convertor'  # переходник


class ConstructionType(str, enum.Enum):
    """Конструкция объектива."""
    ZOOM = 'zoom'  # Зум
    PRIME = 'prime'  # Фикс


class FilterMountType(str, enum.Enum):
    """Тип крепления фильтра."""
    SCREW_IN = 'screw_in'  # Резьбовой
    DROP_IN = 'drop_in'  # Вставной
    REAR_GEL = 'rear_gel'  # Крепление для пленочного фильтра
    NONE = 'none'  # Без крепления


class LensType(str, enum.Enum):
    """Тип объектива."""
    MACRO = 'macro'  # Макро
    FISHEYE = 'fisheye'  # Рыбий глаз
    TILT_SHIFT = 'tilt_shift'  # Смещение оси
    SUPER_TELEPHOTO = 'super_telephoto'  # Длиннофокусный
    WIDE_ANGLE = 'wide_angle'  # Широкоугольный
    STANDARD = 'standard'  # Стандартный
    PORTRAIT = 'portrait'  # Портретный
    CINE = 'cine'  # Кинообъектив
    PANCAKE = 'pancake'  # Блинчик
    THERMAL_LENS = 'thermal_lens'  # Объектив для тепловизора


class TypeDiaphragm(str, enum.Enum):
    """Тип диафрагмы."""
    ELECTRONIC = 'electronic'  # Электронная
    MECHANICAL = 'mechanical'  # Механическая
    MANUAL = 'manual'  # Ручная
    CAMERA_CONTROLLED = 'camera_controlled'  # Управляемая камерой


class FocusType(str, enum.Enum):
    INTERNAL = 'internal'  # Внутренняя фокусировка, габариты объектива обычно не меняются
    FRONT = 'front'  # Фокусировка передней группой линз
    REAR = 'rear'  # Фокусировка задней группой линз
    UNIT = 'unit'  # Фокусировка всей оптической группы / блока
    FLOATING = 'floating'  # Плавающая система, несколько групп двигаются для коррекции аберраций
    EXTENDING = 'extending'  # При фокусировке объектив физически выдвигается
    ROTATING_FRONT = 'rotating_front'  # Передняя часть/резьба под фильтр вращается при фокусировке
    FIXED = 'fixed'  # Фиксированный фокус, фокусировки как механизма нет
    OTHER = 'other'  # Нестандартный/неизвестный тип


class AutofocusMotorType(str, enum.Enum):
    STEPPER = "stepper"  # Шаговый мотор
    ULTRASONIC = "ultrasonic"  # Ультразвуковой мотор
    LINEAR = "linear"  # Линейный мотор
    VOICE_COIL = "voice_coil"  # Voice coil / катушечный линейный привод
    PIEZO = "piezo"  # Пьезо-мотор
    DC = "dc"  # Обычный DC-микромотор
    SCREW_DRIVE = "screw_drive"  # Отверточный привод от камеры
    NONE = "none"  # Нет мотора автофокуса
    OTHER = "other"  # Другое / неизвестно


class ZoomType(str, enum.Enum):
    ROTARY = 'rotary'  # кольцо зума
    PUSH_PULL = 'push_pull'  # тромбон / push-pull
    POWER_ZOOM = 'power_zoom'  # моторизированный зум
    NON_ZOOM = 'non_zoom'  # Без зума, фикс



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

