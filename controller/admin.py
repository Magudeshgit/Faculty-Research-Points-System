from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

admin.site.site_header = "Staff Research Points"
admin.site.register([criteria, achievements, rewardcategory])
