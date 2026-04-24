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
    DIRECT = 'direct'
    WITH_CONVERTOR = 'with_convertor'
