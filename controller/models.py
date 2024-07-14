from django.db import models
from central.models import publication

class criteria(models.Model):
    serial = models.CharField(unique=True, max_length=10, null=False)
    description = models.TextField()
    points = models.PositiveIntegerField()
    
    def __str__(self):
        return self.serial
    
    class Meta:
        verbose_name = "Rewarding Criteria"
        verbose_name_plural = "Rewarding Criterias"
        
class pending(models.Model):
    proposal = models.OneToOneField(publication, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, editable=True)
    
    def __str__(self):
        return str(self.proposal)
    
    class Meta:
        verbose_name = "Pending Proposal"
        verbose_name_plural = "Pending Proposals"