from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

User = settings.AUTH_USER_MODEL


class Network(models.Model):
    network_id = models.CharField(primary_key=True, max_length=100, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = JSONField(default={})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.data.get('label')) or self.network_id
