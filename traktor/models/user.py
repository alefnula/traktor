from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Traktor custom user model."""

    @classmethod
    def get_superuser(cls) -> "User":
        user = cls.objects.filter(is_superuser=True).first()
        if user is not None:
            return user

        return cls.objects.create_superuser(
            username="admin", email="admin@traktor.app"
        )

    @classmethod
    def get_superuser_id(cls) -> int:
        return cls.get_superuser().id

    class Meta(AbstractUser.Meta):
        app_label = "traktor"
