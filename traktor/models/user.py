from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Traktor custom user model."""

    class Meta(AbstractUser.Meta):
        app_label = "traktor"
