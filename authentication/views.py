from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

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
