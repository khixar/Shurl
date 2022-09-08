from uuid import uuid4
from django.db import models


class ModelWithUUID(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True,
                            db_index=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
