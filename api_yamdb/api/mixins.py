from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)


class ListCreateDestroyMixin(
    ListModelMixin, CreateModelMixin, DestroyModelMixin
):
    pass
