from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Exercise(models.Model):
    exercise_id = models.CharField(unique=True, max_length=100, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=400, blank=True, null=True)
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
        return self.label or self.exercise_id
