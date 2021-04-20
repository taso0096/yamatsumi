from django.db import models
from cyberspaces.models import Cyberspace


class Exercise(models.Model):
    cyberspace = models.ForeignKey(Cyberspace, on_delete=models.CASCADE)
    score_url = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    teams = models.JSONField(default=dict, blank=True, null=True)
    users = models.JSONField(default=dict, blank=True, null=True)
    levels = models.JSONField(default=dict, blank=True, null=True)
    categories = models.JSONField(default=dict, blank=True, null=True)
    questions = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cyberspace.id or self.id
