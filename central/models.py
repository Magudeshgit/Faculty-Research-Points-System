from django.db import models
from authentication.models import staff

class publication(models.Model):
    publication = models.CharField(max_length=50) #Temproary
    title = models.CharField(max_length=50)
    identification = models.CharField(verbose_name='ISSN/DOI No',max_length=25)
    url = models.CharField(verbose_name='URL', max_length=50, null=True)
    authors = models.ManyToManyField(staff)
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    Controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.title
    