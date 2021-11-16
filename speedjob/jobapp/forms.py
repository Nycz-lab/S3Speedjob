from django import forms

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
