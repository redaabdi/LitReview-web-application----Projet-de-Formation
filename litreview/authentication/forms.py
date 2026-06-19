from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget = forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirmez le mot de passe", widget = forms.PasswordInput)
    lepede = 'lepedenoumero1'

