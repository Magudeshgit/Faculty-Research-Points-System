from django.db.models.signals import post_save
from django.conf import settings
from central.models import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist


def achievement_saved(sender, instance, **kwargs):
    print(sender._meta.model.__name__)
    if kwargs['created']:
        print('BYE')
    else:
        rc = rewardcategory.objects.get(name=instance._meta.model.__name__)
        obj = achievements.objects.get(achievementid=instance.id, category=rc)
        
        if instance.hodapproval:
            obj.approvalstatus = 'HoD Approved'
            obj.save()
        if instance.controller:
            obj.approvalstatus = 'Controller Approved'
            obj.save() 
    
post_save.connect(achievement_saved, sender=publication)
post_save.connect(achievement_saved, sender=phd)
post_save.connect(achievement_saved, sender=consultancy)
post_save.connect(achievement_saved, sender=funding)
post_save.connect(achievement_saved, sender=ipr)
post_save.connect(achievement_saved, sender=r1)
post_save.connect(achievement_saved, sender=r2)
post_save.connect(achievement_saved, sender=r3)
post_save.connect(achievement_saved, sender=awards)
post_save.connect(achievement_saved, sender=d1)