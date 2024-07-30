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
AY = "01/06/"

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
    # Divide points for ipr based oncount
    for staff in staffs:
        rp = rewardpoints.objects.create(
            staff = staff,
            rc=rc,
            achid=_instance,
            points = calculated_points
        )
        rp.rctr.add(cr)
        rp.save()
        
def add_r3points(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='r3')
    criterias = rc.criterias.all()
    cr = ''
    
    for criteria in criterias:
        print(criteria.description, str(instance.category +' '+instance.mode))
        if criteria.description == str(instance.category +' '+instance.mode):
            calculated_points += criteria.points
            cr = criteria
    
    rp = rewardpoints.objects.create(
        staff=instance.staffs,
        rc=rc,
        achid=_instance,
        points=calculated_points
    )
    rp.rctr.add(cr)
    rp.save()
    
def add_awardpoints(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='awards')
    criterias = rc.criterias.all()
    cr = ''
    # Special Case: referencing serial instead of description
    for criteria in criterias:
        print(criteria.serial, instance.institutiontype)
        if criteria.serial == instance.institutiontype:
            calculated_points += criteria.points
            cr = criteria
            
    rp = rewardpoints.objects.create(
        staff=instance.staffs,
        rc=rc,
        achid=_instance,
        points=calculated_points
    )
    rp.rctr.add(cr)
    rp.save()
    
def add_r1points(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='r1')
    criterias = rc.criterias.all()
    cr = ''
    # Special Case: referencing serial instead of description
    for criteria in criterias:
        # print(criteria.serial, instance.institutiontype)
        if criteria.description == instance.timeperiods:
            calculated_points += criteria.points
            cr = criteria
            
    rp = rewardpoints.objects.create(
        staff=instance.staffs,
        rc=rc,
        achid=_instance,
        points=calculated_points
    )
    rp.rctr.add(cr)
    rp.save()
            
def add_r2points(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='r2')
    criterias = rc.criterias.all()
    cr = ''
    
    # Special Case: referencing serial instead of description
    for criteria in criterias:
        print(criteria.description, instance.duration)
        if criteria.description == instance.duration:
            calculated_points += criteria.points
            cr = criteria
            
    rp = rewardpoints.objects.create(
        staff=instance.staffs,
        rc=rc,
        achid=_instance,
        points=calculated_points
    )
    rp.rctr.add(cr)
    rp.save()

def add_domaincertpoints(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='d1')
    criterias = rc.criterias.all()
    cr = ''
    
    # Special Case: referencing serial instead of description
    for criteria in criterias:
        calculated_points += criteria.points
        cr = criteria
            
    rp = rewardpoints.objects.create(
        staff=instance.staffs,
        rc=rc,
        achid=_instance,
        points=calculated_points
    )
    rp.rctr.add(cr)
    rp.save()
    
def add_phdpoints(_instance):
    calculated_points = 0
    instance = centralmodels[_instance.category.name].objects.get(id=_instance.achievementid)
    
    rc = rewardcategory.objects.get(name='phd')
    criterias = rc.criterias.all()
    cr = ''
    
    for criteria in criterias:
        if criteria.description == instance.type:
            calculated_points +=criteria.points
            cr = criteria
    _staffs = instance.staffs.all()
    # Supervisor Score
    rp = rewardpoints.objects.create(
        staff=instance.supervisor,
        rc=rc,
        achid=_instance,
        points = calculated_points*_staffs.count()
    )
    rp.rctr.add(cr)
    rp.save()
    
    # Staff Score
    for staff in _staffs:
        rp = rewardpoints.objects.create(
        staff=staff,
        rc=rc,
        achid=_instance,
        points = calculated_points
    )
    rp.rctr.add(cr)
    rp.save()