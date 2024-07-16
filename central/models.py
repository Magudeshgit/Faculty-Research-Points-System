from django.db import models
from authentication.models import staff, department

class publication(models.Model):
    publication = models.CharField(max_length=50) #Temproary
    title = models.CharField(max_length=50)
    identification = models.CharField(verbose_name='ISSN/DOI No',max_length=25)
    url = models.CharField(verbose_name='URL', max_length=50, null=True)
    authors = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    date = models.DateField(verbose_name='Date of publication')
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    Controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.title
    
# Consultancy and fundings
class consultancy(models.Model):
    categories = [
        ("consultancy", "consultancy"),
        ("funding", "funding")
    ]
    category = models.CharField(max_length=25, choices=categories)
    
    name = models.CharField(max_length=50)
    agency = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    amount = models.PositiveIntegerField()
    staffs = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    
    # Funding specific
    types = [
        ('sanctioned', 'sanctioned'),
        ('granted', 'granted')
    ]
    status = models.CharField(max_length=10, choices=types, blank=True, null=True)
    receivedamount = models.PositiveIntegerField(null=True, blank=True)
    uc = models.BooleanField(default=False, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Consultancies and fundings'
        verbose_name_plural = 'Consultancies and fundings'