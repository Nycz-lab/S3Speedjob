from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Company, JobOffer, Tag

from django.db.models import Q

class RegisterForm(forms.ModelForm):
    company_name = forms.CharField(label="Company Name", max_length=50)
    company_description = forms.CharField(label="Company Description", max_length=200, widget=forms.Textarea)
    company_address_city = forms.CharField(label="Company City", max_length=50)
    company_address_plz = forms.CharField(label="Company PLZ", max_length=50)
    company_address_street = forms.CharField(label="Company Street", max_length=50)


    class Meta:
        model = Company
        fields = ['company_name', 'company_description', 'company_address_city', 'company_address_plz', 'company_address_street']

class RegisterJobOfferForm(forms.ModelForm):

    company = forms.ModelChoiceField(queryset=Company.objects.none())

    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile')
        super(RegisterJobOfferForm, self).__init__(*args, **kwargs)
        self.fields["company"].queryset = Company.objects.filter(profile=profile, company_approved=True)

    class Meta:
        model = JobOffer
        fields = ['company', 'offer_description', 'tag']
        exclude = ['offer_date']

    tag = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple

    )    

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['image', 'tag', 'gender', 'age', 'type']

    tag = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.all(),
        widget = forms.CheckboxSelectMultiple

    )
