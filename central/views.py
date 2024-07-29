from django.shortcuts import render, redirect
from django.http.response import JsonResponse, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import consultancy, ipr as _ipr, phd as _phd, r1 as _r1, awards as _awards, r2 as _r2, r3 as _r3, publication as publ, funding as _funding, d1 as _d1
from controller.models import achievements, rewardcategory, rewardpoints
from authentication.models import staff, department as dept
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from . import model as coursemodel

# Course Verifier ML MODEL
@csrf_exempt
def verifycourse(request, keyword):
    if request.method == 'POST':
        prediction = coursemodel.predict([keyword])
        if prediction:
            return JsonResponse({"keyword":keyword, "prediction": True})
        else:
            return JsonResponse({"keyword":keyword, "prediction": False})
    else:
        return HttpResponse("This is a API only endpoint")

@login_required
def home(request):
    achievement_count = achievements.objects.filter(staff=request.user, approvalstatus='Controller Approved').count()
    score = rewardpoints.objects.filter(staff=request.user).aggregate(Sum('points'))['points__sum']
    pending_count = achievements.objects.filter(Q(approvalstatus='Not Approved') | Q(approvalstatus='HoD Approved'), staff=request.user).count()
    context = {'ach_count': achievement_count, 'pen_count':pending_count, 'score': score}
    return render(request, 'central/home2.html', context)

@login_required
def submitted(request, id):
    return render(request, 'central/submitted.html', {'obj': id})


# Publication
@login_required
def publication(request):
    publications = publ.objects.filter(Q(authors=request.user) | Q(guide=request.user), controller=True)
    print(request.user.groups)
    return render(request, 'central/publication.html', {"publications": publications})

@login_required
def publication_application(request):
    context = {'error': '', 'title': '', 'publication':'', 'doi': '', 'issn': '' ,'url': '', 'authorcount': '', 'submitted': False}
    data = {}
    staffobj = []
    guide = None
    formfields = ['title','publication', 'doi', 'issn', 'url','date', 'staffcount']
    if request.method == 'POST':
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
            else:
                if request.POST['guideid'] != '':
                        guide = staff.objects.get(username=request.POST['guideid'])
                try:
                    for i in range(1,int(request.POST[field])+1):
                        _username = request.POST['authorid' + str(i)]
                        if request.POST['guideid'] == _username:
                            context = {'error' : 'The Guide ID and Author IDs Cannot be same', 'errorhelp': "Kindly correct the errors below."}
                            return render(request, 'central/publication_application.html', context)

                        _staff = staff.objects.get(username=_username)
                        staffobj.append(_staff)
                except (ObjectDoesNotExist) as e:
                    context = {
                        'errorhelp': 'Kindly correct the errors below',
                        'error': f'Specified Employee ID or Guide ID of staffs: {_username} is invalid or does not exist',
                    }
                    return render(request, 'central/publication_application.html', context)
                
        _department = request.POST['department']
        try:
            department = dept.objects.get(name = _department)
            
            obj = publ.objects.create(**data)
            obj.authors.add(*staffobj)
            obj.guide = guide
            obj.department = department
            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='publication')
            
            ach = achievements.objects.create(
                title=data['title'], 
                achievementid=obj.id,date=data['date'],
                category=rc, department=department)
            ach.staff.add(*staffobj)
            
            # Intentionally Saving macro(consultancy) object after micro(acheievement) object because, 
            # it internally triggers a signal to the micro object which in turn requires 
            # the macro object to saved first.
            
            ach.save()
            obj.save()
            
                
        except IntegrityError:
            context = {
                        'errorhelp': 'Kindly correct the errors below',
                        'iderror': f'The specified DOI or ISSN No has already been registered',
                    }
            return render(request, 'central/publication_application.html', context)
            
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/publication_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
    return render(request, 'central/publication_application.html')

    # Consultancy

# Consultancy
@login_required
def consultancies(request):
    consultancies = consultancy.objects.filter(staffs=request.user, controller=True)
    return render(request, 'central/consultancy.html', {"objects": consultancies})

@login_required
def consultancy_application(request):
    if request.method == 'POST':
        print(request.POST)
        context = {}
        data = {}
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
            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='consultancy')
            ach = achievements.objects.create(
                title=data['name'],achievementid=obj.id,
                date=data['enddate'],category=rc,
                department=department
                )
            ach.staff.add(*staffobj)
            ach.save()
            # Intentionally Saving macro(consultancy) object after micro(acheievement) object because, 
            # it internally triggers a signal to the micro object which in turn requires 
            # the macro object to saved first.
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
@login_required
def funding(request):
    fundings = _funding.objects.filter(staffs=request.user, controller=True)
    return render(request, 'central/funding.html', {"objects": fundings})

@login_required
def funding_application(request):
    if request.method == 'POST':
        context = {}
        data = {}
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
        pi = staff.objects.get(username=request.POST['piid'])
        
        try:    
            obj = _funding.objects.create(**data)
            obj.pi = pi
            obj.staffs.add(*staffobj)
            obj.department = department
            if request.POST['status'] == 'granted':
                obj.receivedamount = request.POST['receivedamount']
                obj.status = request.POST['status']
                obj.uc = True if request.POST['uc'] == 'yes'  else False
            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='funding')
            ach = achievements.objects.create(
                title=data['name'], achievementid = obj.id,
                date=data['enddate'], category=rc,
                department=department
                )
            ach.staff.add(*staffobj)
            
            ach.save()
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
@login_required
def ipr(request):
    obj = _ipr.objects.filter(staffs = request.user, controller=True)
    return render(request, 'central/ipr.html', {'objects':obj})

@login_required
def ipr_application(request):
    context = {}
    if request.method == 'POST':
        data = {}
        staffobj = []
        formfields = ['title', 'category','uniqueno', 'patentoffice', 'date', 'staffcount']
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
            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='ipr')
            ach = achievements.objects.create(
                title=data['title'], achievementid=obj.id,date=data['date'],
                category=rc, department=department)
            ach.staff.add(*staffobj)
            
            ach.save()
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
@login_required
def phd(request):
    obj = _phd.objects.filter(Q(supervisor=request.user) | Q(staffs=request.user), controller=True).distinct()   
    return render(request, 'central/phd.html', {'objects': obj})

@login_required
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
            
            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='phd')
            
            ach = achievements.objects.create(
                title=data['domain'], achievementid=obj.id,
                date=data['date'],category=rc,
                department=department
                )
            ach.staff.add(*staffobj)
            
            ach.save()
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
@login_required
def r1(request):
    obj = _r1.objects.filter(staffs=request.user, controller=True)
    return render(request, 'central/r1.html', {'objects': obj})

# Start from r1_application:
@login_required
def r1_application(request):
    if request.method == 'POST':
        context = {}
        data = {}
        staffobj = []
        formfields = ['title', 'institution', 'type', 'date', 'timeperiods']
        for field in formfields:
            if field != 'staffcount':
                data[field] = request.POST[field]
                
        department = dept.objects.get(name = request.POST['department'])

        try:
            data['staffs'] = request.user
            obj = _r1.objects.create(**data)
            
            obj.department = department
            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='r1')
            
            ach = achievements.objects.create(title=data['title'], achievementid=obj.id,
                                        date=data['date'],category=rc, 
                                        department=department)
            ach.staff.add(request.user)
            
            ach.save()
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

@login_required
def awards(request):
    obj = _awards.objects.filter(staffs=request.user, controller=True)
    return render(request, 'central/awards.html',{'objects':obj})

@login_required
def awards_application(request):
    if request.method == 'POST':
        context = {}
        data = {}
        
        formfields = ['title', 'institution','institutiontype','date']
        for field in formfields:
            data[field] = request.POST[field]
                
        try:    
            obj = _awards.objects.create(**data)
            obj.staffs = request.user
            obj.department = request.user.dept

            
            # Centralizing for Operation 2
            rc = rewardcategory.objects.get(name='awards')
            
            ach = achievements.objects.create(title=data['title'], achievementid=obj.id,
                                              date=data['date'], category=rc, 
                                              department=request.user.dept,
                                              )
            ach.staff.add(request.user)
            
            ach.save()
            obj.save()
            
            
        except IntegrityError:
            context = {
                'iderror': f'The specified Regiser No is already been registered, kindly recheck.',
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

# Research Related Course (Special Case: Department and staffs are automatically added from request object)
@login_required
def r2(request):
    obj = _r2.objects.filter(staffs = request.user, controller=True)
    return render(request, 'central/r2.html', {'objects':obj})

@login_required
def r2_application(request):
    if request.method == 'POST':
        data = {}
        context = {}
        formfields = ['coursename', 'duration', 'mark', 'institution', 'certificateno', 'date']
        for field in formfields:
                data[field] = request.POST[field]
        try:
            obj = _r2.objects.create(**data)
            obj.staffs = request.user
            obj.department = request.user.dept
            
            if coursemodel.predict([data['coursename']]):
                obj.verification = True
            else:
                obj.verification = False
            
            
            rc = rewardcategory.objects.get(name='r2')
            ach = achievements.objects.create(
                title=data['coursename'],achievementid=obj.id,
                date=data['date'],category=rc,
                department=request.user.dept
                )
            ach.staff.add(request.user)
            
            ach.save()
            obj.save()
            
        except IntegrityError as e:
            print(e)
            context = {
                'iderror': f'The specified Certificate No is already been registered, kindly recheck.',
                'errorhelp' : 'Kindly correct the errors below.'
                }
            return render(request, 'central/r2_application.html', context)  
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/r2_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
            
    return render(request, 'central/r2_application.html')

@login_required
def r3(request):
    obj = _r3.objects.filter(staffs = request.user, controller=True)
    return render(request, 'central/r3.html', {'objects': obj})

@login_required
def r3_application(request):
    if request.method == 'POST':
        data = {}
        context = {}
        formfields = ['location', 'category', 'mode', 'date', 'purpose']
        for field in formfields:
                data[field] = request.POST[field]
        try:
            obj = _r3.objects.create(**data)
            obj.staffs = request.user
            obj.department = request.user.dept
            
            rc = rewardcategory.objects.get(name='r3')
            ach = achievements.objects.create(
                title=data['location'], achievementid=obj.id,
                date=data['date'],category=rc,
                department=request.user.dept
                )
            ach.staff.add(request.user)
            
            ach.save()
            obj.save()
            
        except Exception as e:
            context = {
                'iderror': f'The specified Certificate No is already been registered, kindly recheck.',
                'errorhelp' : 'Kindly correct the errors below.'
                }
            return render(request, 'central/r3_application.html', context)  
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/r3_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
    return render(request, 'central/r3_application.html')
def domaincertifications(request):
    obj = _d1.objects.filter(staffs=request.user)
    return render(request, 'central/d1.html', {'objects':obj})
def domaincert_application(request):
    if request.method=='POST':
        data = {}
        context = {}
        formfields = ['domain', 'noc','certificateno', 'date','mark']
        
        for field in formfields:
                data[field] = request.POST[field]
                
        try:
            obj = _d1.objects.create(**data)
            obj.staffs = request.user
            obj.department = request.user.dept
            
            rc = rewardcategory.objects.get(name='d1')
            ach = achievements.objects.create(
                title=data['domain'], achievementid=obj.id,
                date=data['date'],category=rc,
                department=request.user.dept
                )
            ach.staff.add(request.user)
            
            ach.save()
            obj.save()
            
        except Exception as e:
            print(e)
            context = {
                'iderror': f'The specified Certificate No is already been registered, kindly recheck.',
                'errorhelp' : 'Kindly correct the errors below.'
                }
            return render(request, 'central/domaincert_application.html', context) 
        
        if request.POST['submissiontype'] == 'submit':
            context['submitted'] = True
            context['submittedid'] = obj.id
            return render(request, 'central/domaincert_application.html', context)
        else:
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
        
    return render(request, 'central/domaincert_application.html')