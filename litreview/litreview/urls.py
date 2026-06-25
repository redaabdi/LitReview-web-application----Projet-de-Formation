"""
URL configuration for litreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication import views as authentication_views
from feed import views as feed_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', authentication_views.homepage, name='homepage'),
    path('register/', authentication_views.register, name='register'),
    path('feed/', feed_views.feed, name='feed'),
    path('create_ticket/', feed_views.create_ticket, name='create_ticket'),
    path('logout/', authentication_views.logout_view, name='logout'),
    path('posts/', feed_views.posts, name='posts'),
    path('create_review/', feed_views.create_review, name='create_review')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
