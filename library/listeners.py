
from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import Book

@receiver(post_delete, sender=Book)
def delete_files(sender, instance, **kwargs):
    if instance.file: instance.file.delete()
    if instance.thumbnail: instance.thumbnail.delete()




