from django.db import models

# CAS USER DB MODEL
# Custom model object for Mongo Collection sublet_casuser
class CASUser(models.Model):
	username = models.CharField(max_length=6, primary_key=True)
	first_name = models.CharField(max_length=20,default="",blank=True)
	last_name = models.CharField(max_length=20,default="",blank=True)
	email = models.CharField(max_length=15)
	phone = models.CharField(max_length=10,default="",blank=True)
	first_time = models.BooleanField(default=True)


def specific_upload_path(instance, filename):
    # file will be uploaded to media/<owner>/<filename>
    return 'img_{0}/{1}'.format(instance.owner, filename)

# LISTING DB MODEL
# Custom model object for Mongo Collection sublet_listing
class Listing(models.Model):
	owner = models.CharField(max_length=6, primary_key=True)
	address = models.CharField(max_length=100)
	rent = models.DecimalField(max_digits=6, decimal_places=2)
	bedrooms = models.IntegerField()
	bathrooms = models.IntegerField()
	distance = models.DecimalField(max_digits=3, decimal_places=1)
	imgA = models.ImageField(upload_to=specific_upload_path)
	imgB = models.ImageField(upload_to=specific_upload_path,blank=True,default='img/default.jpg')
	imgC = models.ImageField(upload_to=specific_upload_path,blank=True,default='img/default.jpg')

    