from django.db import models
from exercises.models import Exercise


class Cyberspace(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    version = models.CharField(max_length=10, blank=True, null=True)
    routing_table = models.JSONField(default=dict, blank=True, null=True)
    layers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.exercise.id or self.id
