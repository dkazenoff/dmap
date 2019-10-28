from django.db import models
from django.contrib.auth.models import User

# CAS User Object for Collection in MongoDB
class CASUser(models.Model):
    username = models.CharField(max_length=6, primary_key=True)
    first_name = models.CharField(max_length=20,default="")
    last_name = models.CharField(max_length=20,default="")
    email = models.CharField(max_length=15)
    phone = models.CharField(max_length=10,default="")
    first_time = models.BooleanField(default=True)

# Listing Object for Collection in MongoDB
class SubletListing(models.Model):
    owner = models.CharField(max_length=6, primary_key=True)
    address = models.CharField(max_length=100)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    image = models.ImageField(upload_to = 'sublet_img/', default = 'sublet_img/default.png')
    