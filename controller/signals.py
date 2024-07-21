from django.db.models.signals import post_save
from django.conf import settings
from central.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist


def achievement_saved(sender, instance, **kwargs):
    if kwargs['created']:
        print('BYE')
    else:
        
        obj = achievements.objects.get(achievementid=instance.id)
        if instance.hodapproval:
            obj.approvalstatus = 'HoD Approved'
            obj.save()
        if instance.controller:
            obj.approvalstatus = 'Controller Approved'
            obj.save()
    
post_save.connect(achievement_saved, sender=publication)