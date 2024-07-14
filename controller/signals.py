from django.db.models.signals import post_save
from django.conf import settings
from central.models import *
from .models import pending


def publication_received(sender, created, instance, **kwargs):
    if created:
        pending.objects.create(proposal=instance)
        print("Publication saved!")
    
    
post_save.connect(publication_received, sender=publication,weak=False)