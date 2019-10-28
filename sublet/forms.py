from django import forms

class NewUserForm(forms.Form):
	first = forms.CharField(max_length=100)
	last = forms.CharField(max_length=100)