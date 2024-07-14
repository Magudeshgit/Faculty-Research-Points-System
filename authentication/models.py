from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

class department(models.Model):
    name = models.CharField(max_length=50)
    hod = models.OneToOneField('staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='hod')
    
    def __str__(self):
        return self.name
    
class staff(AbstractUser):
    dept = models.ForeignKey(department, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username