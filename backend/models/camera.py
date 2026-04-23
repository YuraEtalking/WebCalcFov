from backend.core import ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin


class Camera(ActiveMixin, Base, CommonFieldsMixin, TimeFieldsMixin):
    pass
    # TODO подумай над полями, может оформить отдельные странички с доп инфой.