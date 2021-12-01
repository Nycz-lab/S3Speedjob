from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    word = models.CharField(max_length=20)

    def __str__(self):
        return f'#{self.word}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.user.username} Profile'

class Company(models.Model):
    company_name = models.CharField(max_length=50)
    company_description = models.CharField(max_length=200, default = "not provided")
    company_address_city = models.CharField(max_length=200, default = "not provided")
    company_address_plz = models.CharField(max_length=200, default = "not provided")
    company_address_street = models.CharField(max_length=200, default = "not provided")
    company_approved = models.BooleanField(default = False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.company_name

class JobOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    offer_description = models.CharField(max_length=200, default = "not provided")
    offer_date = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company}_{self.id}-{self.tag}"
