from import_export import resources
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget, BooleanWidget
from import_export.fields import Field
from central.models import *
from authentication.models import staff,department

class publicationexport(resources.ModelResource):
    author = Field(
        attribute='authors',
        widget=ManyToManyWidget(staff, field='first_name',separator=', '))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
             
    class Meta:
        model=publication
        fields = ('publication','title','doi','issn','isbn','url','count','author','dept','date')

class consultancyexport(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ManyToManyWidget(staff, field='first_name',separator=', '))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    class Meta:
        model=consultancy
        fields = ('name','agency','startdate','date','amount','staffs','dept','date')
        
class fundingexport(resources.ModelResource):
    pi = Field(
        attribute='pi',
        widget=ForeignKeyWidget(staff, 'first_name'))
    
    staffs = Field(
        attribute='staffs',
        widget=ManyToManyWidget(staff, field='first_name',separator=', '))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    
    class Meta:
        model = funding
        fields = ('name','agency','startdate','date','amount','status','receivedamount','uc','pi','staffs','dept','date')
        
class iprexport(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ManyToManyWidget(staff, field='first_name',separator=', '))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    class Meta:
        model = ipr
        fields = ('category','title','uniqueno','patentoffice','date','dept','staffs')
        
class phdexport(resources.ModelResource):
    supervisor = Field(
        attribute='supervisor',
        widget=ForeignKeyWidget(staff, field='first_name',))
    
    staffs = Field(
        attribute='staffs',
        widget=ManyToManyWidget(staff, field='first_name',separator=', '))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    
    class Meta:
        model = phd
        fields = ('domain', 'type', 'registerno', 'date', 'supervisorno', 'supervisor', 'staffs', 'dept')
        
class r1export(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ForeignKeyWidget(staff, field='first_name'))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    
    class Meta:
        model = r1
        fields = ('title', 'institution', 'type', 'date', 'timeperiods', 'staffs', 'dept')
        
class r2export(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ForeignKeyWidget(staff, field='first_name'))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    
    class Meta:
        model = r2
        fields = ('coursename', 'institution', 'duration', 'mark','date','certificateno','verification','staffs', 'dept')
        
class r3export(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ForeignKeyWidget(staff, field='first_name'))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    class Meta:
        model = r3
        fields = ('location', 'category', 'mode', 'purpose', 'date', 'staffs', 'dept')
        
class awardsexport(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ForeignKeyWidget(staff, field='first_name'))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    
    class Meta:
        model = awards
        fields = ('title', 'institution', 'date','staffs', 'dept')

class d1export(resources.ModelResource):
    staffs = Field(
        attribute='staffs',
        widget=ForeignKeyWidget(staff, field='first_name'))

    dept = Field(
        attribute='department',
        widget=ForeignKeyWidget(department, 'name'))
    
    class Meta:
        model = d1
        fields = ('domain', 'noc', 'mark','certificateno','date', 'staffs','dept')