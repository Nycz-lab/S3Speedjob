from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=50)
    company_description = models.CharField(max_length=200, default = "not provided")
    company_address_city = models.CharField(max_length=200, default = "not provided")
    company_address_plz = models.CharField(max_length=200, default = "not provided")
    company_address_street = models.CharField(max_length=200, default = "not provided")
    company_approved = models.BooleanField(default = False)

    def __str__(self):
        return self.company_name

class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE) #look into this later
    contact_firstName = models.CharField(max_length=50)
    contact_lastName = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=50, default = "not provided")
    contact_email = models.EmailField(max_length=50, default = "not provided")

    def __str__(self):
        return self.contact_lastName + " " + self.contact_firstName

class Appl(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    appl_date = models.DateField(auto_now_add=True)
    appl_ip_addr = models.GenericIPAddressField(unpack_ipv4=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
