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
    for staff in staffs:
        rp = rewardpoints.objects.create(
            staff = staff,
            rc = rc,
            achid = _instance,
            points = calculated_points
            )
        rp.rctr.add(criteria)
        rp.save()