from dataclasses import dataclass
from starlette_admin.fields import FloatField
from starlette.requests import Request
from starlette.datastructures import FormData
from starlette_admin import RequestAction


@dataclass
class CommaToDotFloatField(FloatField):
    async def parse_form_data(
        self, request: Request, form_data: FormData, action: RequestAction
    ):
        value = form_data.get(self.id)
        if isinstance(value, str):
            value = value.replace(',', '.').strip()
        try:
            return float(value)
        except (ValueError, TypeError):
            return None