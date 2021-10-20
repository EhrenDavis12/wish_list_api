from django.db import models
from app_user.models import User
from extentions.models import BassModel


class OwnedModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)

    class Meta:
        abstract = True


class AppGroup(BassModel):
    users = models.ManyToManyField(User, related_name="app_groups", through='GroupMember', blank=True)
    # users = models.ManyToManyField(User, related_name="app_groups", blank=True)
    name = models.TextField(blank=False, null=False, default="UnTitled")
    description = models.CharField(max_length=256, blank=True, null=False, default="")
    is_active = models.BooleanField(null=False, default=True)
    # deactivate_after = models.DateField(blank=True, null=True, editable=True)

    def __str__(self):
        return self.name


class GroupMember(BassModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_group = models.ForeignKey(AppGroup, on_delete=models.CASCADE)
    # invite_reason = models.CharField(max_length=256, null=True, blank=True)
    is_admin = models.BooleanField(null=False, default=False)
    nick_name = models.CharField(max_length=64, null=False, blank=True, default="")

    class Meta:
        unique_together = [["user", "app_group"]]


class WishList(BassModel, OwnedModel):
    app_group = models.ManyToManyField(AppGroup, related_name="app_groups")
    name = models.CharField(max_length=256, blank=False, null=False, default="Unknown")
    public_note = models.CharField(max_length=256, blank=True, null=False, default="")
    private_note = models.CharField(max_length=256, blank=True, null=False, default="")

    def __str__(self):
        return self.name
