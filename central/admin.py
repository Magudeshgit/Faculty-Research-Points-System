from django.contrib import admin
from .models import *


admin.site.register([publication, consultancy, ipr, phd, r1, awards])
