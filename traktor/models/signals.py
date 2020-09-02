from django.dispatch import receiver
from django.db.models.signals import post_save

from traktor.models.project import Project
from traktor.models.task import Task


@receiver(post_save, sender=Project)
def create_default_task(sender, instance, created, **kwargs):
    """Create default task for every project."""
    if created:
        Task.objects.create(
            project=instance,
            name="Default",
            default=True,
            color=instance.color,
        )
