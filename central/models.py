from django.db import models
from authentication.models import staff, department


class publication(models.Model):
    publication = models.CharField(max_length=50) #Temproary
    title = models.CharField(max_length=100)
    identification = models.CharField(verbose_name='ISSN/DOI No',max_length=25, unique=True)
    url = models.CharField(verbose_name='URL', max_length=50, null=True)
    guide = models.ForeignKey(staff, on_delete=models.SET_NULL, null=True, related_name='guide')
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
    categories = [
        ("consultancy", "consultancy"),
        ("funding", "funding")
    ]
    category = models.CharField(max_length=25, choices=categories)
    
    name = models.CharField(max_length=50, unique=True)
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
    
    # Verification process
    hodapproval = models.BooleanField(verbose_name="HoD Approval Status", default=False, null=True)
    Controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Consultancies and fundings'
        verbose_name_plural = 'Consultancies and fundings'
        
class ipr(models.Model):
    types = [
        ('Patent Filing','Patent Filing'),
        ('Patent Grant','Patent Grant'),
        ('Design Filing','Design Filing'),
        ('Design Grant','Design Grant'),
        ('Copyright Filing', 'Copyright Filing'),
        ('Copyright Registered','Copyright Registered'),

        ('copyright', 'copyright'),
        ('trademark', 'trademark'),
        ('patent', 'patent')
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
    Controller = models.BooleanField(verbose_name="Controller Approval Status", default=False, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "IPR"
        verbose_name = "IPR"
        
class phd(models.Model):
    choices = (
        ['Guideship - ongoing', 'Guideship - ongoing'],
        ['Guideship - completed', 'Guideship - completed'],
        ['Ongoing Scholar', 'Ongoing Scholar'],
        ['Completed Scholar', 'Completed Scholar'],
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
    
# Research related attending and awards
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
    staffs = models.ManyToManyField(staff)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Research Related Attending & Awards'
        verbose_name_plural = 'Research Related Attendings & Awards'
    
class awards(models.Model):
     modeltypes = (
        ['Attending', 'Attending'],
        ['Award', 'Award']
    )
     
     institutiontypes = [
         ('from our Institution','from our Institution'),
         ('from top NIRF- ranked government and government-aided academic institutions, NPTEL Star performers/Topper certificate','from top NIRF- ranked government and government-aided academic institutions, NPTEL Star performers/Topper certificate'),
         ('from academic institutions in abroad/ Industry /Scientific bodies', 'from academic institutions in abroad/ Industry /Scientific bodies'),
         ('from Government Agencies-State/ National Awards', 'from Government Agencies-State/ National Awards')
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
        ("Reputed academics institutions abroad top NIRF", "Reputed academics institutions abroad top NIRF etc"),
        ("Industries", "Industries"),
        ("Developed Course modules on Swayam-NPTEL or Coursera (minimum: 1hr)","Developed Course modules Swayam-NPTEL or Coursera (minimum: 1hr)")
    ]
    
    mode = models.CharField(max_length=50, choices=modes)
    category = models.CharField(max_length=100, choices=categories)
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
        
        
