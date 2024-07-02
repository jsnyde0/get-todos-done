from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task

@receiver(post_save, sender=Task)
def set_assignee(sender, instance, created, **kwargs):
    if created and not instance.assignee:
        instance.assignee = instance.author
        instance.save()