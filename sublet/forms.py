from sublet.models import CASUser,Listing
from django import forms

class NewUserForm(forms.ModelForm):
	class Meta:
		model = CASUser
		fields = ['first_name','last_name']

class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		exclude = ['owner']
		widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Sublet address', 'class': 'form-control form-control-lg'}),
            'rent': forms.TextInput(attrs={'placeholder': 'Rent per month', 'class': 'form-control form-control-lg','step':'0.01'}),
            'bedrooms': forms.TextInput(attrs={'placeholder': '# of bedrooms', 'class': 'form-control form-control-lg'}),
            'bathrooms': forms.TextInput(attrs={'placeholder': '# of bathrooms', 'class': 'form-control form-control-lg'}),
            'distance': forms.TextInput(attrs={'placeholder': 'Distance from RPI', 'class': 'form-control form-control-lg','step':'0.1'}),
        }