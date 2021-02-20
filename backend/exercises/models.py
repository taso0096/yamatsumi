from django.db import models
from networks.models import Network


class Exercise(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    version = models.CharField(max_length=10, blank=True, null=True)
    teams = models.JSONField(default=dict, blank=True, null=True)
    users = models.JSONField(default=dict, blank=True, null=True)
    levels = models.JSONField(default=dict, blank=True, null=True)
    categories = models.JSONField(default=dict, blank=True, null=True)
    questions = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.network.id or self.id
