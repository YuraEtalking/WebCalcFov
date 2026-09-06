from __future__ import annotations

from pydantic import BaseModel, Field

from backend.services.exposure_equivalence import CalculationResult


class CameraSettingsIn(BaseModel):
    camera_id: int
    focal_length_mm: float = Field(gt=0)
    aperture: float = Field(gt=0, description='f-number, например 2.8')
    shutter: str = Field(description='"1/125" или секунды: "0.5", "2"')
    iso: float = Field(gt=0)


class ExposureRequest(BaseModel):
    reference: CameraSettingsIn
    targets: list[CameraSettingsIn] = Field(min_length=1, max_length=2)


class SettingsOut(BaseModel):
    focal_length_mm: float
    aperture: float
    shutter_seconds: float
    shutter: str
    iso: float


class CameraOut(BaseModel):
    camera_id: int | None
    camera_name: str
    crop_factor: float | None
    settings: SettingsOut
    ev: float


class ExposureComparisonOut(BaseModel):
    reference_ev: float
    target_ev: float
    delta_ev: float
    direction: str  # darker | lighter | equal


class EquivalentSettingsOut(BaseModel):
    reference_crop_factor: float
    target_crop_factor: float
    ratio: float
    focal_length_mm: float
    aperture: float
    iso: float
    shutter_seconds: float
    shutter: str


class TargetOut(BaseModel):
    camera: CameraOut
    exposure: ExposureComparisonOut
    equivalent: EquivalentSettingsOut | None
    equivalence_unavailable_reason: str | None


class ExposureResponse(BaseModel):
    reference: CameraOut
    targets: list[TargetOut]

    @classmethod
    def from_result(cls, result: CalculationResult) -> 'ExposureResponse':
        def camera_out(c) -> CameraOut:
            s = c.settings
            return CameraOut(
                camera_id=c.camera_id,
                camera_name=c.camera_name,
                crop_factor=c.crop_factor,
                settings=SettingsOut(
                    focal_length_mm=s.focal_length_mm,
                    aperture=s.aperture,
                    shutter_seconds=s.shutter_seconds,
                    shutter=s.shutter_display,
                    iso=s.iso,
                ),
                ev=s.ev,
            )

        targets = []
        for t in result.targets:
            eq = t.equivalent
            targets.append(
                TargetOut(
                    camera=camera_out(t.camera),
                    exposure=ExposureComparisonOut(
                        reference_ev=t.exposure.reference_ev,
                        target_ev=t.exposure.target_ev,
                        delta_ev=t.exposure.delta_ev,
                        direction=t.exposure.direction,
                    ),
                    equivalent=EquivalentSettingsOut(
                        reference_crop_factor=eq.reference_crop_factor,
                        target_crop_factor=eq.target_crop_factor,
                        ratio=eq.ratio,
                        focal_length_mm=eq.focal_length_mm,
                        aperture=eq.aperture,
                        iso=eq.iso,
                        shutter_seconds=eq.shutter_seconds,
                        shutter=eq.shutter_display,
                    ) if eq else None,
                    equivalence_unavailable_reason=t.equivalence_unavailable_reason,
                )
            )
        return cls(reference=camera_out(result.reference), targets=targets)