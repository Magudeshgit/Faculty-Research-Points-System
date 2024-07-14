from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin')
def home(request):
    return render(request, 'central/home.html')

def publication(request):
    return render(request, 'central/publication.html')