from sublet.models import CASUser,Listing
from django import forms

# NEW USER FORM MODEL
# Custom new user form based on CASUser Model
class UserSettingsForm(forms.ModelForm):
	class Meta:
		model = CASUser
		fields = ['first_name','last_name','phone']
		# Widgets modify HTML attributes
		widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control form-control-lg'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control form-control-lg'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control form-control-lg'}),
        }
# The attributes we want rendered on the listing form

# LISTING FORM MODEL
# Custom listing form based on Listing Model
# Excludes owner
class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		exclude = ['owner']	# Filter, since this is already passed in
		# Widgets modify HTML attributes
		widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Sublet address', 'class': 'form-control form-control-lg'}),
            'rent': forms.TextInput(attrs={'placeholder': 'Rent per month (per room)', 'class': 'form-control form-control-lg','step':'0.01'}),
            'bedrooms': forms.TextInput(attrs={'placeholder': '# of bedrooms', 'class': 'form-control form-control-lg'}),
            'bathrooms': forms.TextInput(attrs={'placeholder': '# of bathrooms', 'class': 'form-control form-control-lg'}),
            'distance': forms.TextInput(attrs={'placeholder': 'Distance from RPI', 'class': 'form-control form-control-lg','step':'0.1'}),
        }