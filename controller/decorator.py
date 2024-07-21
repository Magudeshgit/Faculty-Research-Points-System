from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q

def is_moderator(view):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(Q(name='HoD') | Q(name='Controller')).exists():
            return view(request, *args, **kwargs)
        else:
            return HttpResponse("Your are restricted from viewing this page")
    return wrapper