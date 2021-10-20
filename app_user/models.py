from django.contrib.auth.models import AbstractUser
from shortuuidfield import ShortUUIDField


class User(AbstractUser):
    id = ShortUUIDField(primary_key=True, editable=False)
    pass
