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


class OwnedModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class WishList(BassModel, OwnedModel):
    # groups = models.ManyToManyField(AppGroup, related_name="groups")
    name = models.CharField(max_length=256, blank=False, null=False, default="Unknown")
    public_note = models.CharField(max_length=256, blank=True, null=True)
    private_note = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name
