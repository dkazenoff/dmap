from django import forms

class NewUserForm(forms.Form):
	first = forms.CharField(max_length=100)
	last = forms.CharField(max_length=100)


class Listing(forms.Form):
	address = forms.CharField(max_length=100)
	bedrooms = forms.IntegerField()
	bathrooms = forms.IntegerField()
	image = forms.ImageField()