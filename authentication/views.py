from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password, make_password

from .models import staff, department

def signin(request):
    context =  {"error": ""}
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        print(user)
        if user:
            login(request, user)
            return redirect('/')
        else:
            context['error']  = "Your username or password is incorrect"
    return render(request, "authentication/signin.html", context)

def profile(request):
    if request.method == 'POST':
        obj = staff.objects.get(id=request.user.id)
        obj.first_name = request.POST['first_name']
        obj.last_name = request.POST['last_name']
        obj.email = request.POST['email']
        obj.phone = request.POST['phone']
        obj.designation = request.POST['designation']
        
        obj.dept = department.objects.get(name=request.POST['department'])
        obj.save()
        
        context = {'message': "Profile Updated!"}
        return render(request, 'authentication/profile.html', context)
        
    return render(request, 'authentication/profile.html')

def change_password(request):
    if request.method == 'POST':
        oldpassword = request.POST['oldpassword']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
    
        if password1 != password2:
            context = {'error': 'Both passwords should match'}
            return render(request, 'authentication/changepassword.html', context)
        
        if request.user.check_password(oldpassword):
            request.user.set_password(password1)
            request.user.save()
            return redirect('/profile')
        else:
            context = {'error': 'Incorrect old password'}
            return render(request, 'authentication/changepassword.html', context)
            
        
        
    return render(request, 'authentication/changepassword.html')

def _logout(request):
    logout(request)
    return redirect('/')