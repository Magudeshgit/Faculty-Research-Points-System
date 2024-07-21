from django.contrib import admin
from .models import *


admin.site.register([publication, 
                     consultancy, 
                     ipr,
                     phd,
                     awards,
                     r1,
                     r2,
                     r3
                     ])
