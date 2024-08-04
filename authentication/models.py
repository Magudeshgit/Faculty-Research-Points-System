from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class department(models.Model):
    name = models.CharField(max_length=50)
    hod = models.OneToOneField('staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='hod')
    
    def __str__(self):
        return self.name
    
class staff(AbstractUser):
    dept = models.ForeignKey(department, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    
    def get_name(self):
        return self.first_name
    def __str__(self):
        return self.username