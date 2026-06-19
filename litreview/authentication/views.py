from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from authentication import forms

def register_errors(username, password, password_confirm) :
    fields = {"nom d'utilisateur" : username, 'mot de passe' : password, 'confirmation du mot de passe' : password_confirm}
    errors = []
    for key, value in fields.items() :
        if value == '' :
           errors.append(f"Le champ {key} est vide.")
    if password != password_confirm :
        errors.append('Les mots de passe ne correspondent pas')
    if User.objects.filter(username=username).exists() :
        errors.append("Le nom d'utilisateur existe déjà")
    print(errors)
    return errors

def login_errors(username, password) :
    fields = {"nom d'utilisateur" : username, "mot de passe" : password}
    errors = []
    for key, value in fields.items() :
        if value == '' :
            errors.append(f"Veuillez rentrer un {key}.")
    try:
        user = User.objects.get(username=username)
        if user.password != password:
            errors.append("Le mot de passe et le nom d'utilisateur ne correspondent pas")
    except User.DoesNotExist:
        errors.append("L'utilisateur n'existe pas")
    print(errors)
    return errors

def homepage(request):
    if request.method == 'POST' :
        data = request.POST
        errors = login_errors(data.get('username'), data.get('password'))

        if errors :
            return render(request, 'homepage.html', {'errors' : errors})
        else :
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
            User.objects.create(username=data.get('username'),password=data.get('password'))
            return render(request, 'register.html', {'success' : 'Bravo vous êtes enregistré'})
    else :
        return render(request, 'register.html')


    
    
        


