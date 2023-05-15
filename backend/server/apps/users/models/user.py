from django.contrib.auth.models import AbstractUser
from django.db.models import CharField

from common.models import TimeStampedModel

from .managers import UserManager


class User(AbstractUser, TimeStampedModel):
    telegram_id = CharField(max_length=128, unique=True, verbose_name="Telegram id")
    username = CharField(max_length=128, blank=True, null=True, verbose_name="username")
    first_name = CharField(
        max_length=128, blank=True, null=True, verbose_name="first_name"
    )
    photo_url = CharField(
        max_length=128, blank=True, null=True, verbose_name="photo_url"
    )
    USERNAME_FIELD = "telegram_id"
    objects = UserManager()

    def __str__(self):
        return self.username if self.username else self.telegram_id
