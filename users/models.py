from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


from core.models import AbstractBaseModel


# Create your models here.
class User(AbstractUser, AbstractBaseModel):
    token = models.UUIDField(default=uuid4())
