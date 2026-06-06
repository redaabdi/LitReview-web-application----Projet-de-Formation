from django.db import models

class User(models.Model) :
    username = models.fields.CharField(max_length=20)
    password = models.fields.CharField(max_length=20)
