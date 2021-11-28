from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    company_name = forms.CharField(label="Company Name", max_length=50)
    company_description = forms.CharField(label="Company Description", max_length=200, widget=forms.Textarea)
    company_address_city = forms.CharField(label="Company City", max_length=50)
    company_address_plz = forms.CharField(label="Company PLZ", max_length=50)
    company_address_street = forms.CharField(label="Company Street", max_length=50)

    firstName = forms.CharField(label="First Name", max_length=50)
    lastName = forms.CharField(label="Last Name", max_length=50)
    email = forms.EmailField(label="Email", max_length=50)
    phone = forms.CharField(label="Phone", max_length=50, required=False)

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
