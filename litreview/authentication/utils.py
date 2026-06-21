from django.contrib.auth.models import User

def register_errors(username, password, password_confirm) :
    fields = {"nom d'utilisateur" : username, 'mot de passe' : password, 'confirmation du mot de passe' : password_confirm}
    errors = []
    for key, value in fields.items() :
        if value == '' :
           errors.append(f"Le champ {key} est vide.")
    if password != password_confirm :
        errors.append('Les mots de passe doivent être identiques')
    if User.objects.filter(username=username).exists() :
        errors.append("Le nom d'utilisateur existe déjà")
    return errors

def login_errors(username, password) :
    fields = {"nom d'utilisateur" : username, "mot de passe" : password}
    errors = []
    for key, value in fields.items() :
        if value == '' :
            errors.append(f"Veuillez rentrer un {key}.")
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        errors.append("L'utilisateur n'existe pas")
    if not user.check_password(password):
            errors.append("Le mot de passe et le nom d'utilisateur ne correspondent pas")
    print(errors)
    return errors