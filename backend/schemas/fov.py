from pydantic import BaseModel, field_validator


class FovCalcInput(BaseModel):
    camera_id: int
    lens_id: int
    distance: int
    focal: float | None = None
    teleconverter_id: int | None = None

    @field_validator('teleconverter_id', mode='before')
    @classmethod
    def validate_teleconverter_id(cls, value):
        if value in (None, ''):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValueError('Некорректное значение телеконвертера')


    @field_validator('distance', mode='before')
    @classmethod
    def validate_distance(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if not value.isdigit():
                raise ValueError('Дистанция должна быть целым числом')
            distance = int(value)

            if distance <= 0:
                raise ValueError('Дистанция должна быть больше 0')
        return value
