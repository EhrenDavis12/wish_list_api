from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.auth.models import User
import pendulum


class BassModel(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False)
    created = models.DateTimeField(default=pendulum.now, editable=False)
    last_updated = models.DateTimeField(default=pendulum.now, editable=True)

    class Meta:
        ordering = ["created"]
        abstract = True
