from __future__ import annotations

import math
from dataclasses import dataclass
from loguru import logger

# Меньше этой разницы (в стопах) считаем экспозицию совпадающей.
EV_EQUAL_TOLERANCE = 0.05
MAX_TARGETS = 2

REASON_REFERENCE_NO_SENSOR = 'reference_no_sensor'
REASON_TARGET_NO_SENSOR = 'target_no_sensor'


class ExposureInputError(ValueError):
    """Ошибка входных данных. Текст показывается пользователю (не 500)."""



def parse_shutter(raw: str | int | float) -> float:
    """Преобразует выдержку из пользовательского ввода в секунды.

    Принимает: "1/125", "1/125 s", "1/125 с", "0.5", "0,5", "2", "2\"", 0.008.
    """
    # logger.debug('raw данные: raw="{}", type(raw)="{}"', raw, type(raw))
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        value = float(raw)
        # logger.debug('отдаем value: value="{}"', value)
    else:
        text = str(raw).strip().lower().replace(',', '.')
        for junk in ('sec', 'сек', 's', 'с', '"', '″', ' '):
            text = text.replace(junk, '')
        if not text:
            raise ExposureInputError('Shutter speed is required.')
        try:
            if '/' in text:
                numerator, denominator = text.split('/', 1)
                # logger.debug('numerator, denominator: numerator="{}", denominator="{}"', numerator, denominator)
                value = float(numerator) / float(denominator)
            else:
                value = float(text)
        except (ValueError, ZeroDivisionError) as exc:
            raise ExposureInputError(
                f'Invalid shutter speed "{raw}". Use e.g. 1/125 or 0.5.'
            ) from exc

    if not math.isfinite(value) or value <= 0:
        raise ExposureInputError('Shutter speed must be a positive number.')
    # logger.debug('return value: value="{}" , type(value)="{}"', value, type(value))
    return value


def format_shutter(seconds: float) -> str:
    """Форматирует выдержку для отображения: 1/125, 1/2.5, 2, 0.75."""
    if seconds >= 1:
        return f'{seconds:g}'
    denominator = 1 / seconds
    if abs(denominator - round(denominator)) < 1e-6:
        return f'1/{round(denominator)}'
    return f'1/{denominator:.1f}'


@dataclass(frozen=True)
class ExposureSettings:
    """Экспотреугольник + фокусное расстояние для одной камеры."""

    focal_length_mm: float
    aperture: float          # f-number, например 2.8
    shutter_seconds: float   # например 1/125
    iso: float

    def __post_init__(self) -> None:
        for label, value in (
            ('Focal length', self.focal_length_mm),
            ('Aperture', self.aperture),
            ('Shutter speed', self.shutter_seconds),
            ('ISO', self.iso),
        ):
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
                raise ExposureInputError(f'{label} must be a positive number.')

    @property
    def ev(self) -> float:
        """EV с учётом ISO: log2((N² / t) · (100 / ISO))."""
        return exposure_value(self.aperture, self.shutter_seconds, self.iso)

    @property
    def shutter_display(self) -> str:
        return format_shutter(self.shutter_seconds)


@dataclass(frozen=True)
class CameraInput:
    """Камера + введённые для неё настройки."""

    camera_id: int | None
    camera_name: str
    crop_factor: float | None   # None — размеры сенсора неизвестны
    settings: ExposureSettings

    @property
    def has_sensor_size(self) -> bool:
        return self.crop_factor is not None and self.crop_factor > 0



@dataclass(frozen=True)
class ExposureComparison:
    """Результат 1: фактическая разница EV. Размер сенсора не учитывается."""

    reference_ev: float
    target_ev: float
    delta_ev: float  # target_ev - reference_ev

    @property
    def direction(self) -> str:
        """'darker' | 'lighter' | 'equal' — для текста в шаблоне."""
        if abs(self.delta_ev) < EV_EQUAL_TOLERANCE:
            return 'equal'
        return 'darker' if self.delta_ev > 0 else 'lighter'

    @property
    def stops(self) -> float:
        """Разница по модулю, в стопах."""
        return abs(self.delta_ev)


@dataclass(frozen=True)
class EquivalentSettings:
    """Результат 2: эквивалентные настройки для сравниваемой камеры."""

    reference_crop_factor: float
    target_crop_factor: float
    ratio: float                 # C_ref / C_target
    focal_length_mm: float
    aperture: float
    iso: float                   # математически точное, без округления
    shutter_seconds: float       # без изменений

    @property
    def shutter_display(self) -> str:
        return format_shutter(self.shutter_seconds)


@dataclass(frozen=True)
class TargetResult:
    camera: CameraInput
    exposure: ExposureComparison
    equivalent: EquivalentSettings | None
    equivalence_unavailable_reason: str | None  # REASON_* или None


@dataclass(frozen=True)
class CalculationResult:
    reference: CameraInput
    reference_ev: float
    targets: list[TargetResult]


def exposure_value(aperture: float, shutter_seconds: float, iso: float) -> float:
    return math.log2((aperture ** 2 / shutter_seconds) * (100 / iso))


def compare_exposure(
    reference: ExposureSettings,
    target: ExposureSettings,
) -> ExposureComparison:
    reference_ev = reference.ev
    target_ev = target.ev
    return ExposureComparison(
        reference_ev=reference_ev,
        target_ev=target_ev,
        delta_ev=target_ev - reference_ev,
    )


def equivalent_settings(
    reference: ExposureSettings,
    reference_crop_factor: float,
    target_crop_factor: float,
) -> EquivalentSettings:
    ratio = reference_crop_factor / target_crop_factor
    return EquivalentSettings(
        reference_crop_factor=reference_crop_factor,
        target_crop_factor=target_crop_factor,
        ratio=ratio,
        focal_length_mm=reference.focal_length_mm * ratio,
        aperture=reference.aperture * ratio,
        iso=reference.iso * ratio ** 2,
        shutter_seconds=reference.shutter_seconds,
    )


def calculate(reference: CameraInput, targets: list[CameraInput]) -> CalculationResult:
    """Главная точка входа: считает оба результата для каждой сравниваемой камеры."""
    if not targets:
        raise ExposureInputError('Add at least one camera to compare.')
    if len(targets) > MAX_TARGETS:
        raise ExposureInputError(f'You can compare at most {MAX_TARGETS} cameras.')

    results: list[TargetResult] = []
    for target in targets:
        exposure = compare_exposure(reference.settings, target.settings)

        equivalent: EquivalentSettings | None = None
        reason: str | None = None
        if not reference.has_sensor_size:
            reason = REASON_REFERENCE_NO_SENSOR
        elif not target.has_sensor_size:
            reason = REASON_TARGET_NO_SENSOR
        else:
            equivalent = equivalent_settings(
                reference.settings,
                reference.crop_factor,   # type: ignore[arg-type]
                target.crop_factor,      # type: ignore[arg-type]
            )

        results.append(
            TargetResult(
                camera=target,
                exposure=exposure,
                equivalent=equivalent,
                equivalence_unavailable_reason=reason,
            )
        )

    return CalculationResult(
        reference=reference,
        reference_ev=reference.settings.ev,
        targets=results,
    )