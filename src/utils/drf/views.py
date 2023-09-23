"""
Utils drf views.
"""
from rest_framework import viewsets, mixins


class ModelCRUViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    Base modelviewset for CRU operations.
    """
    pass
