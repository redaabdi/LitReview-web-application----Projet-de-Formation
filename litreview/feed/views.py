from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url = 'homepage')
def feed(request) :
    return render(request, 'feed.html')

def ticket_create(request) :
    return render(request, 'ticket_create.html')
