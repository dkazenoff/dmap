"""Module to represent the models to be used in the mongodb"""
from django.db import models

# CAS USER DB MODEL
# Custom model object for Mongo Collection sublet_casuser
class CASUser(models.Model):
    """Model to represent CAS user information"""
    username = models.CharField(max_length=6, primary_key=True)
    first_name = models.CharField(max_length=20, default="", blank=True)
    last_name = models.CharField(max_length=20, default="", blank=True)
    email = models.CharField(max_length=15)
    phone = models.CharField(max_length=10, default="", blank=True)
    first_time = models.BooleanField(default=True)


# LISTING DB MODEL
# Custom model object for Mongo Collection sublet_listing
class Listing(models.Model):
    """Model to represent a listing"""
    list_id = models.CharField(max_length=32, primary_key=True)
    owner = models.ForeignKey(CASUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    rent = models.DecimalField(max_digits=6, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    distance = models.DecimalField(max_digits=3, decimal_places=1)
    form_completion = models.BooleanField(default=False)
    img_completion = models.BooleanField(default=False)

# IMAGE DB MODEL
# Custom model object for Mongo Collection sublet_image
class Image(models.Model):
    """Model to represent an image in the db"""
    img_id = models.CharField(max_length=32, primary_key=True, default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    c_type = models.CharField(max_length=50)
    data = models.BinaryField(blank=True)
    size = models.PositiveIntegerField(default=0)
