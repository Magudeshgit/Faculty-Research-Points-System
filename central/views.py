from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import publication as publ
from .models import consultancy
from authentication.models import staff, department as dept
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url='/signin')
def home(request):
    return render(request, 'central/home.html')

def submitted(request, id):
    return render(request, 'central/submitted.html', {'obj': id})

# Publication
def publication(request):
    publications = publ.objects.filter(authors=request.user)
    print(request.user.groups)
    return render(request, 'central/publication.html', {"publications": publications})

def publication_application(request):
    context = {'error': '', 'title': '', 'index':'', 'identification': '', 'url': '', 'authorcount': ''}
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
            context['title'] = title
            context['index'] = index
            context['identification'] = identification
            context['url'] = url
            context['authorcount'] = authorcount
            return render(request, 'central/publication_application.html', context)
        print(authorsobj)
        print(department)
            
        paper = publ.objects.create(publication=index, 
                            title=title,
                            identification = identification,
                            url=url,
                            department=department,
                            date=date
                            )
        
        paper.authors.add(*authorsobj)
        paper.save()
        
        return redirect(reverse('submitted', kwargs={'id': paper.id}))
        
        
    return render(request, 'central/publication_application.html', context)

    # Consultancy

# Consultancy
def consultancies(request):
    consultancies = consultancy.objects.filter(staffs=request.user, category="consultancy")
    return render(request, 'central/consultancy.html', {"objects": consultancies})

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
                        'staffcount': request.POST['staffcount']
                    }
                    return render(request, 'central/consultancy_application.html', context)
                
        _department = request.POST['department']
        
        
        department = dept.objects.get(name = _department)
        obj = consultancy.objects.create(**data)
        obj.staffs.add(*staffobj)
        obj.department = department
        obj.save()
        return redirect(reverse('submitted', kwargs={'id': obj.id}))
        
    return render(request, 'central/consultancy_application.html')

#Start with Funding
def funding(request):
    fundings = consultancy.objects.filter(staffs=request.user, category='funding')
    print(fundings)
    return render(request, 'central/funding.html', {"objects": fundings})

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
            return redirect(reverse('submitted', kwargs={'id': obj.id}))
        except ValueError:
            context = {
                        'error': f'We are facing issue submitting your application, try rechecking the fields and submit again. If this issue persists, contact IT Support (ERR_CODE: 001VAL)',
                        'name': data['name'],
                        'agency': data['agency'],
                        'startdate': data['startdate'],
                        'enddate': data['enddate'],
                        'amount': data['amount'],
                        'staffcount': request.POST['staffcount']
                    }
            return render(request, 'central/consultancy_application.html', context)
        
    return render(request, 'central/funding_application.html')