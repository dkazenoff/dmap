"""sddproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from sublet import views
import cas.views

urlpatterns = [
    path('', views.landing, name='Sublet Landing Page'),
    path('sublet/', views.home, name='home'),
    path('sublet/create', views.create, name='create'),
    path('sublet/view', views.view, name='view'),
    path('sublet/newuser/', views.newuser, name='register'),
    path('sublet/login/', cas.views.login, name='login'),
    # Does not redirect back from CAS on localhost
	path('sublet/logout/', cas.views.logout, name='logout'),
]
