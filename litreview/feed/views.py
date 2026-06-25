from django.shortcuts import render, redirect
from .models import Ticket, Review, UserFollows
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm

@login_required(login_url = 'homepage')
def feed(request) :
    return render(request, 'feed.html')

@login_required(login_url = 'homepage')
def create_ticket(request) :
    if request.method == 'POST' : 
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid() :
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return render(request, 'create_ticket.html', {'success' : 'Bravo votre demande à bien été publié'})
        else : 
            return render(request, 'create_ticket.html', {'ticket_form' : ticket_form})
    else :
        return render(request, 'create_ticket.html')

@login_required(login_url = 'homepage')
def create_review(request):
    if request.method == 'POST' :
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid() :
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
        else :
            return render(request, 'create_review.html', {"ticket_form" : ticket_form})
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            
            
            return render(request, 'create_review.html', {'success' : 'Bravo votre critique à bien été publié !'})
        else : 
            return render(request, 'create_review.html', {"review_form" : review_form})
    else :
        return render(request, 'create_review.html')

@login_required(login_url = 'homepage')
def posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    posts = sorted(tickets, key=lambda post: post.time_created, reverse=True)
    return render(request, 'posts.html', context={'posts' : posts})
