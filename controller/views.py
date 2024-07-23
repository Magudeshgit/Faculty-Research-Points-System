from django.shortcuts import render, redirect
from central.models import *
from .models import *
from .decorator import is_moderator
from django.db.models import Q
from django.contrib import messages

# Dependency function
# Note: Variable names are file names changing them will cause template not found error
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

@is_moderator
def approvalapplication(request, category,id):
    obj = centralmodels[category].objects.get(id=id)
    return render(request, f'controller/applications/{category}_application.html', {'object': obj})

@is_moderator
def pendingapprovals(request):
    if request.user.groups.filter(name='HoD').exists():
        objects = achievements.objects.filter(Q(approvalstatus='Not Approved'), Q(department=request.user.dept)).distinct()
    else:
        objects = achievements.objects.filter(approvalstatus='HoD Approved')
    return render(request, 'controller/pendingapprovals.html', {'objects':objects})

@is_moderator
def approve(request, category, id):
    print(request.path_info)
    obj = centralmodels[category].objects.get(id=id)
    if request.user.groups.filter(name='HoD').exists():
        obj.hodapproval = True
    elif request.user.groups.filter(name='Controller').exists():
        obj.controller = True
    obj.save()
    messages.success(request, 'Proposal Approved!')
    return redirect('/pendingapprovals')