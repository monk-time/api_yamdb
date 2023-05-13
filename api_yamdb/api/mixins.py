from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)


class ListCreateDestroyMixin(
    ListModelMixin, CreateModelMixin, DestroyModelMixin
):
    pass
