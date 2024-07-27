from .models import rewardcategory, rewardpoints
from central.models import *

centralmodels = {
    'publication': publication,
    'consultancy': consultancy,
    'funding': funding,
    'ipr': ipr,
    'phd': phd,
    'r1': r1,
    'r2': r2,
    'r3': r3,
    'awards': awards,
    'd1': d1
}

def add_publicationpoints(_instance):
    # Criteria: Publication index and no of staff members
    calculated_points = 0
    divident = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='publication')
    criterias = rc.criterias.all()
    criteria = ''
    
    
    # C1 - Publication index
    for _criteria in criterias:
        if instance.publication == _criteria.description:
            calculated_points += _criteria.points
            criteria = _criteria
    
    # C2 - Staff Members
    
    staffs = instance.authors.all()
    divident = calculated_points / staffs.count() 
    for staff in staffs:
        rp = rewardpoints.objects.create(
            staff = staff,
            rc = rc,
            achid = _instance,
            points = divident
            )
        rp.rctr.add(criteria)
        rp.save()
        
def add_consultancypoints(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    rc = rewardcategory.objects.get(name='consultancy')
    criterias = rc.criterias.all()
    for criteria in criterias:
        calculated_points+=criteria.points
    
    # Staff Points
    
    for staff in instance.staffs.all():
        rp = rewardpoints.objects.create(
            staff=staff,
            rc=rc,
            achid=_instance,
            points = calculated_points * (instance.amount/10000)
        )
        rp.rctr.add(criteria)
        rp.save()
    
def add_fundingpoints(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    rc = rewardcategory.objects.get(name='funding')
    criterias = rc.criterias.all()
    
    for criteria in criterias:
        if criteria.description == instance.status:
            calculated_points+=criteria.points
    
    if instance.status == 'sanctioned':
        # For PI
        rp = rewardpoints.objects.create(
                staff=instance.pi,
                rc = rc,
                achid = _instance,
                points = calculated_points * (instance.amount/10000) 
        )
        rp.rctr.add(criteria)
        rp.save()
        
        # For CO-PI
        for staff in instance.staffs.all():
            rp = rewardpoints.objects.create(
                staff=staff,
                rc=rc,
                achid=_instance,
                points = (calculated_points/2) * (instance.amount/10000)
            )
            rp.rctr.add(criteria)
            rp.save()
    else:
        rp = rewardpoints.objects.create(
                staff=instance.pi,
                rc = rc,
                achid = _instance,
                points = calculated_points
        )
        rp.rctr.add(criteria)
        rp.save()
        
        # For CO-PI
        for staff in instance.staffs.all():
            rp = rewardpoints.objects.create(
                staff=staff,
                rc=rc,
                achid=_instance,
                points = 2
            )
            rp.rctr.add(criteria)
            rp.save()
            
def add_iprpoints(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='ipr')
    criterias = rc.criterias.all()
    cr = ''
    
    for criteria in criterias:
        print(criteria.description, instance.category)
        if criteria.description == instance.category:
            calculated_points += criteria.points
            cr = criteria
            
    staffs = instance.staffs.all()
    calculated_points = calculated_points / staffs.count()
    
    for staff in staffs:
        rp = rewardpoints.objects.create(
            staff = staff,
            rc=rc,
            achid=_instance,
            points = calculated_points
        )
        rp.rctr.add(cr)
        rp.save()