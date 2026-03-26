from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'license_number', 'phone', 'address', 'age']


class VehicleRegistrationForm(forms.Form):
    """Form for users to register their vehicle for alerts"""
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your mobile number',
            'pattern': '[0-9]{10}',
            'title': 'Enter 10-digit mobile number'
        })
    )
    vehicle_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter vehicle number (e.g., DL 2S G 5988)',
            'style': 'text-transform: uppercase;'
        })
    )
