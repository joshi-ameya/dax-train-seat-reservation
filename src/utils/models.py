"""
Util app models.
"""
import uuid
from django.db import models


class BaseCustomModel(models.Model):
    """
    Abstract model for id and timestamps.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
