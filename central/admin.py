from django.contrib import admin
from .models import *


admin.site.register([publication, 
                     consultancy, 
                     funding,
                     ipr,
                     phd,
                     awards,
                     r1,
                     r2,
                     r3,
                     d1
                     ])
