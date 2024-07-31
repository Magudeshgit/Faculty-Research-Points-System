from django.db import models
from authentication.models import staff, department

# r1 - Research related attendings STTP/FDP
# r2 - Research related course certifications
# r3 - Acted as a resource person

class publication(models.Model):
    publication = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    
    doi = models.CharField(verbose_name='ISSN No',max_length=25, unique=True, null=True)
    issn = models.CharField(verbose_name='DOI No',max_length=25, unique=True, null=True)
    isbn = models.CharField(verbose_name='ISBN No', max_length=25, unique=True, null=True)
    url = models.CharField(verbose_name='URL', max_length=50, null=True)
    
    count = models.PositiveIntegerField()
    authors = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    date = models.DateField(verbose_name='Date of publication')
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.title 
    
# Consultancy and fundings
class consultancy(models.Model):
    name = models.CharField(max_length=50, unique=True)
    agency = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    amount = models.PositiveIntegerField()
    staffs = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Consultancy'
        verbose_name_plural = 'Consultancies'

class funding(models.Model):
    name = models.CharField(max_length=50, unique=True)
    agency = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    amount = models.PositiveIntegerField()
    
    pi = models.ForeignKey(staff, related_name='pi', on_delete=models.SET_NULL, null=True)
    staffs = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    
    types = [
        ('sanctioned', 'sanctioned'),
        ('submitted', 'submitted')
    ]
    status = models.CharField(max_length=10, choices=types, blank=True, null=True)
    receivedamount = models.PositiveIntegerField(null=True, blank=True)
    uc = models.BooleanField(default=False, blank=True)
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Funding'
        verbose_name_plural = 'Fundings'

class ipr(models.Model):
    types = [
        ('Patent Filing','Patent Filing'),
        ('Patent Granted','Patent Granted'),
        ('Design Filing','Design Filing'),
        ('Design Granted','Design Granted'),
        ('Copyright Filing', 'Copyright Filing'),
        ('Copyright Registered','Copyright Registered')
]
    category = models.CharField(max_length=50, choices=types)
    title = models.CharField(max_length=100)
    uniqueno = models.CharField(max_length=50, unique=True) #Change CharField to somethingelse if required
    patentoffice = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    staffs = models.ManyToManyField(staff)
    status = models.CharField(max_length=50, null=True, blank=True,choices=[('filing', 'filing'),('granted', 'granted')])
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "IPR"
        verbose_name = "IPR"
        
class phd(models.Model):
    choices = (
        ['Ongoing', 'Ongoing'],
        ['Completed', 'Completed'],
        )
    type = models.CharField(max_length=50, choices=choices)
    domain = models.CharField(max_length=50)
    registerno = models.CharField(max_length=50, unique=True)    #Inquire about where to put unique constraint
    date = models.DateField()
    supervisorno = models.CharField(max_length=50)
    supervisor = models.ForeignKey(staff, on_delete=models.SET_NULL, related_name='supervisor', null=True)    
    staffs = models.ManyToManyField(staff)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.domain


# Single User objects
# Research related attending
class r1(models.Model):
    types = (
        ['STTP','STTP'],
        ['FDP', 'FDP  (NPTEL excluded)'],
        ['Seminar', 'Seminar'],
        ['Workshop', 'Workshop'],
    )
    timeperiods = (
        ['Upto 2 days', 'Upto 2 days'],
        ['Upto 1 week', 'Upto 1 week'],
        ['2 weeks and above', '2 weeks and above'],
    )

    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=50)
    date = models.DateField()
    type = models.CharField(max_length=25, choices=types)
    timeperiods = models.CharField(max_length=50, choices=timeperiods)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    staffs = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True)
    
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Research Related Attending (STTP/FDP)'
        verbose_name_plural = 'Research Related Attendings (STTP/FDP)'

class awards(models.Model):
     modeltypes = (
        ['Attending', 'Attending'],
        ['Award', 'Award']
    )
     
     institutiontypes = [
         ('RC029','RC029'),
         ('RC030','RC030'),
         ('RC031', 'RC031'),
         ('RC032', 'RC032')
     ]
     
     title = models.CharField(max_length=100)
     institution = models.CharField(max_length=100)
     institutiontype = models.CharField(max_length=150, choices=institutiontypes)
     date = models.DateField()
     department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
     staffs = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True)
     
     hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
     controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
     
     def __str__(self):
         return self.title
     
     class Meta:
         verbose_name = 'Award'
         verbose_name_plural = 'Awards'
         
# Research Related Course (Special Case)
class r2(models.Model):
    durations = [
        ("Succesfully completed 4 weeks", "Succesfully completed 4 weeks"),
        ("Succesfully completed 8 weeks", "Succesfully completed 8 weeks"),
        ("Succesfully completed 12 weeks", "Succesfully completed 12 weeks")
    ]
    coursename = models.CharField(max_length=50)
    duration = models.CharField(max_length=50, choices=durations)
    mark = models.PositiveIntegerField()
    institution = models.CharField(max_length=75)
    certificateno = models.CharField(max_length=35, unique=True)
    staffs = models.ForeignKey(staff, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    verification = models.BooleanField(null=True)
    date = models.DateField()
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    
    class Meta:
        verbose_name = 'Research Related Course'
        verbose_name_plural = 'Research Related Courses'
    
    def __str__(self):
        return self.coursename

# Acted as a resource person
class r3(models.Model):
    modes = [
        ("Online", "Online"),
        ("Offline", "Offline"),
    ]
    categories = [
        ("reputed institutions abroad",
         "reputed institutions abroad"),
        ("industries", "industries"),
        ("course modules", "course modules")
    ]
    
    mode = models.CharField(max_length=50, choices=modes)
    category = models.TextField(choices=categories)
    location = models.CharField(max_length=75)
    purpose = models.TextField()
    staffs = models.ForeignKey(staff, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    class Meta:
        verbose_name = 'Acted as a Resource person'
        verbose_name_plural = 'Acted as a Resource person'
    
    def __str__(self):
        return self.location
        
class d1(models.Model):
    domain = models.CharField(max_length=50)
    noc = models.PositiveIntegerField()
    mark = models.PositiveIntegerField()
    certificateno = models.CharField(max_length=35, unique=True)
    staffs = models.ForeignKey(staff, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(department, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    
    class Meta:
        verbose_name = 'Domain Certification'
        verbose_name_plural = 'Domain Certifications'
    
    def __str__(self):
        return self.domain