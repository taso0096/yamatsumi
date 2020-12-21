from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

import uuid

User = settings.AUTH_USER_MODEL


class Network(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField(default={})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.data.get('label')) or str(self.data.get('id')) or self.id
