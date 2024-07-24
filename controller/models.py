from typing import Iterable
from django.db import models
from authentication.models import staff
from central.models import *

centralmodels = {
    'publication': publication,
    'consultancy': consultancy,
    'funding': funding,
    'ipr': ipr,
    'phd': phd,
    'r1': r1,
    'r2': r2,
    'r3': r3,
    'awards': awards,
    'd1': d1
}

class criteria(models.Model):
    serial = models.CharField(unique=True, max_length=10, null=False)
    description = models.TextField()
    points = models.PositiveIntegerField()
    
    def __str__(self):
        return self.serial
    
    class Meta:
        verbose_name = "Rewarding Criteria"
        verbose_name_plural = "Rewarding Criterias"
        
class achievements(models.Model):
    statuses = [
        ('Not Approved', 'Not Approved'),
        ('HoD Approved', 'HoD Approved'),
        ('Controller Approved', 'Controller Approved')
    ]
    title = models.CharField(max_length=150)
    staff = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    achievementid = models.PositiveIntegerField()
    date = models.DateField()
    category = models.ForeignKey('rewardcategory', on_delete=models.SET_NULL, null=True)
    approvalstatus = models.CharField(max_length=50, choices=statuses, default='Not Approved')
    
    def __str__(self):
        return self.title + ' - ' + self.category.name
    
    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "All Acheivements"
        
class rewardcategory(models.Model):
    name = models.CharField(max_length=75)
    criterias = models.ManyToManyField(criteria)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Reward Category'
        verbose_name_plural = 'Reward Categories'
        
class rewardpoints(models.Model):
    staff = models.ForeignKey(staff, on_delete=models.CASCADE)
    rc = models.ForeignKey(rewardcategory, on_delete=models.SET_NULL, null=True, verbose_name="Reward Category")
    achid = models.ForeignKey(achievements, on_delete=models.SET_NULL, null=True, verbose_name='Achievement ID')
    rctr = models.ManyToManyField(criteria, verbose_name='Reward Criteria')
    points = models.PositiveIntegerField()
    
    class Meta:
        verbose_name='Reward Point'
        verbose_name_plural='Reward Points'
    
    