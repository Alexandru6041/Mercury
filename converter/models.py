from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

class FileModel(models.Model):
    nume = models.CharField(max_length=50, unique=True)
    dimensiune = models.FloatField()
    sheet = models.CharField(max_length=20)
    rand_header = models.IntegerField()
    nume_firma = models.CharField(max_length=100)
    cif_firma = models.IntegerField()

    def __str__(self):
        return self.nume

@receiver(post_delete, sender=FileModel)
def signal_function_name(sender, instance, using, **kwargs):
    path = f'input files/{instance.nume}'

    if os.path.exists(path):
        os.remove(path)
