from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Cyberspace(models.Model):
    cyberspace_id = models.CharField(unique=True, max_length=100, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, blank=True, null=True)
    desc = models.CharField(max_length=400, blank=True, null=True)
    scores_url = models.CharField(max_length=100, blank=True, null=True)
    questions_url = models.CharField(max_length=100, blank=True, null=True)
    user_routing_url = models.CharField(max_length=100, blank=True, null=True)
    extra_url = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    routing_table = models.JSONField(default=dict, blank=True, null=True)
    options = models.JSONField()
    layers = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label or self.cyberspace_id
