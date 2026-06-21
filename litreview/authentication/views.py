from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authentication.utils import register_errors, login_errors

def homepage(request):
    if request.method == 'POST' :
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        errors = login_errors(username, password)
        if errors :
            return render(request, 'homepage.html', {'errors' : errors})
        else :
            user_authenticated = authenticate(request, username=username, password=password)
            login(request, user_authenticated)
            return redirect('feed')
    else :
        if request.user.is_authenticated:
            return redirect('feed')
        else :
            return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST' :
        data = request.POST
        errors = register_errors(data.get('username'), data.get('password'), data.get('password_confirm'))
        if errors :
            return render(request, 'register.html', {'errors' : errors})
        else :
            User.objects.create_user(username=data.get('username'),password=data.get('password'))
            return render(request, 'register.html', {'success' : 'Bravo vous êtes enregistré'})
    else :
        return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')


    
    
        


