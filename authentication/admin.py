from typing import Any
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import *


class staffadmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.password = make_password(obj.password)
        return super().save_model(request, obj, form, change)
    
admin.site.register(staff, staffadmin)
admin.site.register(department)