from django.db import models

# CAS USER DB MODEL
# Custom model object for Mongo Collection sublet_casuser
class CASUser(models.Model):
	username = models.CharField(max_length=6, primary_key=True)
	first_name = models.CharField(max_length=20,default="")
	last_name = models.CharField(max_length=20,default="")
	email = models.CharField(max_length=15)
	phone = models.CharField(max_length=10,default="")
	first_time = models.BooleanField(default=True)

# LISTING DB MODEL
# Custom model object for Mongo Collection sublet_listing
class Listing(models.Model):
	owner = models.CharField(max_length=6, primary_key=True)
	address = models.CharField(max_length=100)
	rent = models.DecimalField(max_digits=6, decimal_places=2)
	bedrooms = models.IntegerField()
	bathrooms = models.IntegerField()
	distance = models.DecimalField(max_digits=3, decimal_places=1)

    