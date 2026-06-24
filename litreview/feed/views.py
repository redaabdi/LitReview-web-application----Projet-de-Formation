from django.shortcuts import render, redirect
from .models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from .forms import TicketForm


@login_required(login_url = 'homepage')
def feed(request) :
    return render(request, 'feed.html')

@login_required(login_url = 'homepage')
def ticket_create(request) :
    if request.method == 'POST' : 
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid() :
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return render(request, 'ticket_create.html', {'success' : 'Bravo votre demande à bien été publié'})
        else : 
            return render(request, 'ticket_create.html', {'ticket_form' : ticket_form})
    else :
        return render(request, 'ticket_create.html')

@login_required(login_url = 'homepage')
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)

    posts = sorted(tickets, key=lambda post: post.time_created, reverse=True)
    return render(request, 'posts.html', context={'posts' : posts})
