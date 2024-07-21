"""
URL configuration for analyser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from authentication import views as atv
from central import views as ctv
from controller import views as btv

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication App
    
    path('signin/', atv.signin),
    path('', ctv.home),
    path('submitted/<int:id>/', ctv.submitted, name='submitted'),
    
    # Central App
    
    path('publication/', ctv.publication),
    path('publicationapplication/', ctv.publication_application),
    
    path('consultancy/', ctv.consultancies),
    path('consultancyapplication/', ctv.consultancy_application),
    
    path('funding/', ctv.funding),
    path('fundingapplication/', ctv.funding_application),
    
    path('ipr/', ctv.ipr),
    path('iprapplication/', ctv.ipr_application),
    
    path('phd/', ctv.phd),
    path('phdapplication/', ctv.phd_application),
    
    path('r1/', ctv.r1),
    path('r1application/', ctv.r1_application),
    
    path('r2/', ctv.r2),
    path('r2application/', ctv.r2_application),
    
    path('r3/', ctv.r3),
    path('r3application/', ctv.r3_application),
    
    path('awards/', ctv.awards),
    path('awardapplication/', ctv.awards_application),
    
    # Controller App
    
    path('approvalapplication/<str:category>/<int:id>/', btv.approvalapplication, name="approvalapplication"),
    
    path('pendingapprovals/', btv.pendingapprovals),
    path('approve/<str:category>/<int:id>/', btv.approve, name='approve'),
]