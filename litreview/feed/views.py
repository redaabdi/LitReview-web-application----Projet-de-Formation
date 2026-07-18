from django.shortcuts import render, redirect
from .models import Ticket, Review
from django.contrib.auth.models import User
from follows.models import UserFollows, UserBlocks
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm
from itertools import chain
from django.db.models import Value, CharField, Q


@login_required(login_url="homepage")
def feed(request):
    tickets = get_tickets_feed(request.user)
    reviews = get_reviews_feed(request.user)

    feed = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(request, "feed.html", {"feed": feed})


@login_required(login_url="homepage")
def create_review_response(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return render(
                request,
                "create_review_response.html",
                {"ticket": ticket, "success": "Votre critique a bien été publié !"},
            )
        else:
            return render(
                request,
                "create_review_response.html",
                {"ticket": ticket, "review_form": review_form},
            )

    else:

        return render(request, "create_review_response.html", {"ticket": ticket})


@login_required(login_url="homepage")
def create_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return render(
                request,
                "create_ticket.html",
                {"success": "Bravo votre demande à bien été publié"},
            )
        else:
            return render(request, "create_ticket.html", {"ticket_form": ticket_form})
    else:
        return render(request, "create_ticket.html")


@login_required(login_url="homepage")
def create_review(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return render(
                request,
                "create_review.html",
                {"success": "Bravo votre critique à bien été publié !"},
            )
        else:
            return render(
                request,
                "create_review.html",
                {"ticket_form": ticket_form, "review_form": review_form},
            )
    else:
        return render(request, "create_review.html")


@login_required(login_url="homepage")
def posts(request):
    if request.method == "POST" and request.POST.get("action") == "delete":
        data = request.POST
        content_type = data.get("content_type")
        pk = data.get("pk")
        if content_type == "TICKET":
            Ticket.objects.filter(pk=pk, user=request.user).delete()
        elif content_type == "REVIEW":
            Review.objects.filter(pk=pk, user=request.user).delete()
        return redirect("posts")
    else:
        tickets = Ticket.objects.filter(user=request.user)
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
        reviews = Review.objects.filter(user=request.user)
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
        posts = sorted(
            chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
        )
        return render(request, "posts.html", context={"posts": posts})


@login_required(login_url="homepage")
def edit_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk, user=request.user)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            if request.POST.get("delete-image-boolean") == "true":
                ticket.image.delete()
            ticket.save()
            return render(
                request,
                "edit_ticket.html",
                {"ticket": ticket, "success": "Bravo votre ticket à bien été modifié"},
            )
        else:
            return render(
                request,
                "edit_ticket.html",
                {"ticket": ticket, "ticket_form": ticket_form},
            )
    else:
        return render(request, "edit_ticket.html", {"ticket": ticket})


@login_required(login_url="homepage")
def edit_review(request, pk):
    review = Review.objects.get(pk=pk, user=request.user)
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES, instance=review.ticket)
        review_form = ReviewForm(request.POST, instance=review)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket_user = request.POST.get("user")
            ticket.user = User.objects.get(username=ticket_user)
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return render(
                request,
                "edit_review.html",
                {
                    "review": review,
                    "success": "Bravo votre critique à bien été modifié",
                },
            )
        else:
            return render(
                request,
                "edit_review.html",
                {
                    "ticket_form": ticket_form,
                    "review_form": review_form,
                    "review": review,
                },
            )
    return render(request, "edit_review.html", {"review": review})


def get_tickets_feed(user):
    users_i_follow = [
        relation_user_i_follow.followed_user
        for relation_user_i_follow in UserFollows.objects.filter(user=user)
    ]
    users_to_include = users_i_follow + [user]
    tickets_feed = Ticket.objects.filter(user__in=users_to_include).annotate(
        content_type=Value("TICKET", CharField())
    )

    for post in tickets_feed:
        post.already_reviewed = Review.objects.filter(ticket=post, user=user).exists()

    return tickets_feed


def get_reviews_feed(user):
    users_i_blocked = [
        relation.blocked_user for relation in UserBlocks.objects.filter(user=user)
    ]
    users_blocked_me = [
        relation.user for relation in UserBlocks.objects.filter(blocked_user=user)
    ]
    users_blocked = users_i_blocked + users_blocked_me

    users_i_follow = [
        relation.followed_user for relation in UserFollows.objects.filter(user=user)
    ]
    users_to_include = users_i_follow + [user]

    reviews_feed = Review.objects.filter(
        Q(user__in=users_to_include) & ~Q(ticket__user__in=users_blocked)
        | Q(ticket__user=user) & ~Q(user__in=users_blocked)
    )
    reviews_feed = reviews_feed.annotate(content_type=Value("REVIEW", CharField()))

    for post in reviews_feed:
        post.ticket.already_reviewed = Review.objects.filter(
            ticket=post.ticket, user=user
        ).exists()

    return reviews_feed
