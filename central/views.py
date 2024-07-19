from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import publication as publ
from .models import consultancy, ipr as _ipr, phd as _phd, r1 as _r1, awards as _awards
from authentication.models import staff, department as dept
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q

@login_required(login_url='/signin')
def home(request):
    return render(request, 'central/home.html')

@login_required(login_url='/signin')
def submitted(request, id):
    return render(request, 'central/submitted.html', {'obj': id})


# Publication
@login_required(login_url='/signin')
def publication(request):
    publications = publ.objects.filter(authors=request.user)
    print(request.user.groups)
    return render(request, 'central/publication.html', {"publications": publications})

@login_required(login_url='/signin')
def publication_application(request):
    context = {'error': '', 'title': '', 'index':'', 'identification': '', 'url': '', 'authorcount': '', 'submitted': False}
    if request.method == 'POST':
        
        try:
            print(request.POST)
            title = request.POST['title']
            index = request.POST['index']
            identification = request.POST['identification']
            url = request.POST['url']
            authorcount= request.POST['authorcount']
            guideid = request.POST['guideid']
            department = request.POST['department']
            date = request.POST['date']
            authorsobj = []
        except Exception as e:
            print(e)
            
        
        try:
            for i in range(1,int(authorcount)+1):
                _username = request.POST['authorid' + str(i)]
                author = staff.objects.get(username=_username)
                authorsobj.append(author)
            department = dept.objects.get(name = department)
        except ObjectDoesNotExist:
            context['error'] = f'Specified Employee ID of staffs: {_username} is invalid or does not exist'
            context['errorhelp'] = 'Kindly correct the errors below.'
            context['title'] = title
            context['index'] = index
            context['identification'] = identification
            context['url'] = url
            context['authorcount'] = authorcount
            return render(request, 'central/publication_application.html', context)
        print(authorsobj)
        print(department)
        
        try:
            paper = publ.objects.create(publication=index, 
                                title=title,
                                identification = identification,
                                url=url,
                                department=department,
                                date=date
                                )
        
            paper.authors.add(*authorsobj)
            paper.save()
        except Exception as e:
            context['iderror'] = f'The specified DOI/ISSN No is already been registered by another staff member, kindly recheck.'
            context['errorhelp'] = 'Kindly correct the errors below.'
            context['title'] = title
            context['index'] = index
            context['identification'] = identification
            context['url'] = url
            context['authorcount'] = authorcount
            return render(request, 'central/publication_application.html', context)
            
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = paper.id
            return render(request, 'central/publication_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': paper.id}))
    return render(request, 'central/publication_application.html', context)

    # Consultancy

# Consultancy
@login_required(login_url='/signin')
def consultancies(request):
    consultancies = consultancy.objects.filter(staffs=request.user, category="consultancy")
    return render(request, 'central/consultancy.html', {"objects": consultancies})

@login_required(login_url='/signin')
def consultancy_application(request):
    if request.method == 'POST':
        print(request.POST)
        context = {}
        data = {'category':'consultancy'}
        staffobj = []
        formfields = ['name', 'agency', 'startdate', 'enddate', 'amount', 'staffcount']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except ObjectDoesNotExist:
                    context = {
                        'error': f'Specified Employee ID of staffs: {_username} is invalid or does not exist',
                        'name': data['name'],
                        'agency': data['agency'],
                        'startdate': data['startdate'],
                        'enddate': data['enddate'],
                        'amount': data['amount'],
                    }
                    return render(request, 'central/consultancy_application.html', context)
                
        _department = request.POST['department']
        
        try:
            department = dept.objects.get(name = _department)
            obj = consultancy.objects.create(**data)
            obj.staffs.add(*staffobj)
            obj.department = department
            obj.save()
        except IntegrityError:
            context = {
                        'errorhelp': f'The specified name of the consultancy has already been registered',
                    }
            return render(request, 'central/consultancy_application.html', context)
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/consultancy_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
            
    return render(request, 'central/consultancy_application.html')

# Funding
@login_required(login_url='/signin')
def funding(request):
    fundings = consultancy.objects.filter(staffs=request.user, category='funding')
    print(fundings)
    return render(request, 'central/funding.html', {"objects": fundings})

@login_required(login_url='/signin')
def funding_application(request):
    if request.method == 'POST':
        print(request.POST)
        context = {}
        data = {'category':'funding'}
        staffobj = []
        formfields = ['name', 'agency', 'startdate', 'enddate', 'amount', 'status' ,'staffcount']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except ObjectDoesNotExist:
                    context = {
                        'error': f'Specified Employee ID of staffs: {_username} is invalid or does not exist',
                        'name': data['name'],
                        'agency': data['agency'],
                        'startdate': data['startdate'],
                        'enddate': data['enddate'],
                        'amount': data['amount'],
                        'status': data['status'],
                        'receivedamount': request.POST['receivedamount'],
                        'uc': request.POST['uc'],
                        'staffcount': request.POST['staffcount']
                    }
                    return render(request, 'central/funding_application.html', context)
            
        _department = request.POST['department']
        department = dept.objects.get(name = _department)
        
        try:    
            obj = consultancy.objects.create(**data)
            obj.staffs.add(*staffobj)
            obj.department = department
            if request.POST['status'] == 'granted':
                obj.receivedamount = request.POST['receivedamount']
                obj.status = request.POST['status']
                obj.uc = True if request.POST['uc'] == 'yes'  else False
            obj.save()
        except IntegrityError:
            context = {
                'errorhelp': f'The specified name of the funding has already been registered',
                }
            return render(request, 'central/funding_application.html', context)            
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/funding_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
    return render(request, 'central/funding_application.html')

# IPR Related
@login_required(login_url='/signin')
def ipr(request):
    obj = _ipr.objects.filter(staffs = request.user)
    return render(request, 'central/ipr.html', {'objects':obj})

@login_required(login_url='/signin')
def ipr_application(request):
    context = {}
    if request.method == 'POST':
        data = {}
        staffobj = []
        formfields = ['title', 'category', 'status', 'uniqueno', 'patentoffice', 'date', 'staffcount']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except ObjectDoesNotExist:
                    context = {
                        'errorhelp' :'Kindly correct the errors below and recheck all the fields',
                        'error': f'Specified Employee ID of staffs: {_username} is invalid or does not exist',
                        'title': data['title'],
                        'category': data['category'],
                        'status': data['status'],
                        'uniqueno': data['uniqueno'],
                        'patentoffice': data['patentoffice'],
                        'date': data['date'],
                        'staffcount': request.POST['staffcount'],
                    }
                    return render(request, 'central/ipr_application.html', context)
                
        department = dept.objects.get(name = request.POST['department'])
        try:    
            obj = _ipr.objects.create(**data)
            obj.staffs.add(*staffobj)
            obj.department = department
            obj.save()
        except IntegrityError:
            context = {
                'iderror': f'The specified Unique No is already been registered by another staff member, kindly recheck.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/ipr_application.html', context)     
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/funding_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
    return render(request, 'central/ipr_application.html')

# PhD Related
@login_required(login_url='/signin')
def phd(request):
    obj = _phd.objects.filter(Q(supervisor=request.user) | Q(staffs=request.user)).distinct()   
    return render(request, 'central/phd.html', {'objects': obj})

@login_required(login_url='/signin')
def phd_application(request):
    context = {}
    if request.method == 'POST':
        data={}
        staffobj = []
        formfields = ['domain', 'type', 'registerno', 'supervisorno', 'date', 'staffcount']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except ObjectDoesNotExist:
                    context = {
                        'errorhelp' :'Kindly correct the errors below and recheck all the fields',
                        'error': f'Specified Employee ID of staffs: {_username} is invalid or does not exist',
                    }
                    return render(request, 'central/phd_application.html', context)
        
        department = dept.objects.get(name = request.POST['department'])
        try:    
            supervisor = staff.objects.get(username = request.POST['supervisorid'])
            obj = _phd.objects.create(**data)
            obj.staffs.add(*staffobj)
            obj.department = department
            obj.supervisor = supervisor
            obj.save()
        except IntegrityError:
            context = {
                'iderror': f'The specified Regiser No is already been registered, kindly recheck.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/phd_application.html', context)  
        except ObjectDoesNotExist:
            context = {
                'supervisorerror': f'The specified Employee ID of supervisor is not valid or it does not exist.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/phd_application.html', context)  
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/phd_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
                
    return render(request, 'central/phd_application.html')


# Research oriented STTP/FDP (NPTEL excluded)/ Seminar/Workshop attended (Physical mode & External only)
@login_required(login_url='/signin')
def r1(request):
    obj = _r1.objects.filter(staffs=request.user)
    return render(request, 'central/r1.html', {'objects': obj})

# Start from r1_application:
@login_required(login_url='/signin')
def r1_application(request):
    if request.method == 'POST':
        context = {}
        data = {}
        staffobj = []
        formfields = ['title', 'institution', 'type', 'date', 'timeperiods','staffcount']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except ObjectDoesNotExist:
                    context = {
                        'errorhelp' :'Kindly correct the errors below and recheck all the fields',
                        'error': f'Specified Employee ID of staffs: {_username} is invalid or does not exist',
                        'title': data['title'],
                        'category': data['category'],
                        'status': data['status'],
                        'uniqueno': data['uniqueno'],
                        'patentoffice': data['patentoffice'],
                        'date': data['date'],
                        'staffcount': request.POST['staffcount'],
                    }
                    return render(request, 'central/r1_application.html', context)
                
        department = dept.objects.get(name = request.POST['department'])
        try:    
            obj = _r1.objects.create(**data)
            obj.staffs.add(*staffobj)
            obj.department = department
            obj.save()
        except IntegrityError:
            context = {
                'iderror': f'The specified Regiser No is already been registered, kindly recheck.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/r1_application.html', context)  
        except ObjectDoesNotExist:
            context = {
                'supervisorerror': f'The specified Employee ID of supervisor is not valid or it does not exist.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/r1_application.html', context)  
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/r1_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
        
        
    return render(request, 'central/r1_application.html')

@login_required(login_url='/signin')
def awards(request):
    obj = _awards.objects.filter(staffs=request.user)
    return render(request, 'central/awards.html',{'objects':obj})

@login_required(login_url='/signin')
def awards_application(request):
    if request.method == 'POST':
        context = {}
        data = {}
        staffobj = []
        
        formfields = ['title', 'institution','institutiontype','date','staffcount']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except ObjectDoesNotExist:
                    context = {
                        'errorhelp' :'Kindly correct the errors below and recheck all the fields',
                        'error': f'Specified Employee ID of staffs: {_username} is invalid or does not exist',
                        'title': data['title'],
                        'category': data['category'],
                        'status': data['status'],
                        'uniqueno': data['uniqueno'],
                        'patentoffice': data['patentoffice'],
                        'date': data['date'],
                        'staffcount': request.POST['staffcount'],
                    }
                    return render(request, 'central/awards_application.html', context)
                
        department = dept.objects.get(name = request.POST['department'])
        try:    
            obj = _awards.objects.create(**data)
            obj.staffs.add(*staffobj)
            obj.department = department
            obj.save()
        except IntegrityError:
            context = {
                'iderror': f'The specified Regiser No is already been registered, kindly recheck.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/awards_application.html', context)  
        except ObjectDoesNotExist:
            context = {
                'supervisorerror': f'The specified Employee ID of supervisor is not valid or it does not exist.',
                'errorhelp' :'Kindly correct the errors below.'
                }
            return render(request, 'central/awards_application.html', context)  
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/awards_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
        
        
    return render(request, 'central/awards_application.html')