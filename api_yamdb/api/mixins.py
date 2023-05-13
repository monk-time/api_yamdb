from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)


class ListCreateDestroyViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin
):
    pass
