"""Module to define forms for use by the website"""
from django import forms
from sublet.models import CASUser, Listing


# NEW USER FORM MODEL
# Custom new user form based on CASUser Model
class UserSettingsForm(forms.ModelForm):
    """Class to represent form for user information"""
    class Meta:
        """Meta class asked for by django"""
        model = CASUser
        # Fields to include
        fields = ['first_name', 'last_name', 'phone', 'email']
        # Widgets modify HTML attributes
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name', 'class':
                                                 'form-control form-control-lg'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name', 'class':
                                                'form-control form-control-lg'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class':
                                            'form-control form-control-lg'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email Address', 'class':
                                            'form-control form-control-lg'}),}

# LISTING FORM MODEL
# Custom listing form based on Listing Model
# Excludes owner
class ListingForm(forms.ModelForm):
    """Class to represent form for a listing"""
    class Meta:
        """Meta class asked for by django"""
        model = Listing
        # Fields to disregard
        exclude = ['list_id', 'owner', 'form_completion', 'img_completion']
        # Widgets modify HTML attributes
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Sublet address',
                                              'class': 'form-control form-control-lg'}),
            'rent': forms.TextInput(attrs={'placeholder': 'Rent per month (per room)',
                                           'class': 'form-control form-control-lg', 'step':'0.01'}),
            'bedrooms': forms.TextInput(attrs={'placeholder': '# of bedrooms',
                                               'class': 'form-control form-control-lg'}),
            'bathrooms': forms.TextInput(attrs={'placeholder': '# of bathrooms',
                                                'class': 'form-control form-control-lg'}),
            'distance': forms.TextInput(attrs={'placeholder': 'Distance from RPI',
                                               'class': 'form-control form-control-lg',
                                               'step':'0.1'}),}

class ImageForm(forms.Form):
    """Class to represent form for image upload"""
    sublet_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
