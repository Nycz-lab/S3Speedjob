from django.db import models
from django.contrib.auth.models import User

# Create your models here.

User._meta.get_field('email')._unique = True    # set email field on user table to unique so that a email can only be used once

GENDER_CHOICES = (
(1, ('Male')),
(2, ('Female')),
(3, ('Other'))
)

AFFILIATION_CHOICES = (
(1, ('Employee')),
(2, ('Company-Employer'))
)

class Tag(models.Model):
    word = models.CharField(max_length=20)  # hashtag for tagging

    def __str__(self):
        return f'#{self.word}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 1-1 relationship
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    tag = models.ManyToManyField(Tag, blank=True)   # n to n relationship
    gender = models.PositiveSmallIntegerField(('gender'),
                                                choices = GENDER_CHOICES,
                                                blank=True,
                                                null=True)
    age = models.IntegerField(blank=False, null=True)
    type = models.PositiveSmallIntegerField(('affiliation'),
                                                choices = AFFILIATION_CHOICES,
                                                blank = False,
                                                null = False,
                                                default = 1)


    def __str__(self):
        return f'{self.user.username} Profile'

class Company(models.Model):
    company_name = models.CharField(max_length=50)
    company_description = models.CharField(max_length=200, default = "not provided")
    company_address_city = models.CharField(max_length=200, blank = False, null = False)
    company_address_plz = models.IntegerField(blank = False, null = False)
    company_address_street = models.CharField(max_length=200, blank = False, null = False)
    company_approved = models.BooleanField(default = False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE) # 1 to n relationship

    def __str__(self):
        return self.company_name

class JobOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    offer_description = models.CharField(max_length=200, default = "not provided")
    offer_date = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.CASCADE) # 1 to n relationship

    def __str__(self):
        return f"{self.company}_{self.id}-{self.tag}"
