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
from django.conf import settings
from django.conf.urls.static import static 
from sublet import views
import cas.views

urlpatterns = [
    path('', views.landing, name='Sublet Landing Page'),
    path('sublet/', views.home, name='home'),
    path('sublet/manage/', views.listing_menu, name='list_menu'),
    path('sublet/manage/create/', views.create_listing, name='list_create'),
    path('sublet/manage/<str:list_id>', views.listing_menu, name='list_specific'),
    path('sublet/manage/<str:list_id>/delete/', views.delete_listing, name='list_delete'),
    path('sublet/manage/<str:list_id>/update/', views.update_listing, name='list_update'),
    path('sublet/manage/<str:list_id>/upload/', views.upload_images, name='image_upload'),
    path('sublet/manage/<str:list_id>/<str:img_id>/delete', views.delete_image, name='image_delete'),
    path('sublet/listings/', views.listing_info, name='view_all'),
    path('sublet/listings/<str:sort_by>', views.listing_info, name='view_all'),
    path('sublet/view/<str:list_id>', views.view_list, name='list_view'),
    path('sublet/usermenu/', views.user_menu, name='setting'),
    path('sublet/login/', cas.views.login, name='login'),
    # Does not redirect back from CAS on localhost
	path('sublet/logout/', cas.views.logout, name='logout'),
]