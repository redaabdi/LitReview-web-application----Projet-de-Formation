from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserFollows, UserBlocks
from django.contrib.auth.models import User
from django.db import IntegrityError


@login_required(login_url="homepage")
def follows(request):
    relations_userfollows = UserFollows.objects.filter(user=request.user)
    relations_userisfollowed = UserFollows.objects.filter(followed_user=request.user)
    relations_userblocks = UserBlocks.objects.filter(user=request.user)

    if request.method == "POST":
        data = request.POST
        if data.get("action") == "follow":
            try:
                followed_username = data.get("username")
                followed_user = User.objects.get(username=followed_username)
            except User.DoesNotExist:
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Utilisateur introuvable",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            if followed_user == request.user:
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Vous ne pouvez pas vous suivre vous-même",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            if UserBlocks.objects.filter(
                user=followed_user, blocked_user=request.user
            ).exists():
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Utilisateur introuvable",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            if UserBlocks.objects.filter(
                user=request.user, blocked_user=followed_user
            ).exists():
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Cet utilisateur est bloqué",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            try:
                UserFollows.objects.create(
                    user=request.user, followed_user=followed_user
                )
            except IntegrityError:
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Vous suivez déjà cet utilisateur !",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            return render(
                request,
                "follows.html",
                {
                    "message": "Vous suivez désormais cet utilisateur !",
                    "relations_userfollows": relations_userfollows,
                    "relations_userisfollowed": relations_userisfollowed,
                    "relations_userblocks": relations_userblocks,
                },
            )
        elif data.get("action") == "unfollow":
            relation_id = data.get("relation_id")
            relation = UserFollows(id=relation_id)
            relation.delete()
            return render(
                request,
                "follows.html",
                {
                    "message": "Vous vous êtes désabonné cet utilisateur !",
                    "relations_userfollows": relations_userfollows,
                    "relations_userisfollowed": relations_userisfollowed,
                    "relations_userblocks": relations_userblocks,
                },
            )
        elif data.get("action") == "block":
            try:
                blocked_username = data.get("username")
                blocked_user = User.objects.get(username=blocked_username)
            except User.DoesNotExist:
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Utilisateur introuvable",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            try:
                UserBlocks.objects.create(user=request.user, blocked_user=blocked_user)
            except IntegrityError:
                return render(
                    request,
                    "follows.html",
                    {
                        "message": "Utilisateur déjà bloqué",
                        "relations_userfollows": relations_userfollows,
                        "relations_userisfollowed": relations_userisfollowed,
                        "relations_userblocks": relations_userblocks,
                    },
                )
            if UserFollows.objects.filter(
                user=request.user, followed_user=blocked_user
            ).exists():
                UserFollows.objects.filter(
                    user=request.user, followed_user=blocked_user
                ).delete()
            if UserFollows.objects.filter(
                user=blocked_user, followed_user=request.user
            ).exists():
                UserFollows.objects.filter(
                    user=blocked_user, followed_user=request.user
                ).delete()
        elif data.get("action") == "unblock":
            relation_id = data.get("relation_id")
            relation = UserBlocks(id=relation_id)
            relation.delete()
    return render(
        request,
        "follows.html",
        {
            "relations_userfollows": relations_userfollows,
            "relations_userisfollowed": relations_userisfollowed,
            "relations_userblocks": relations_userblocks,
        },
    )
