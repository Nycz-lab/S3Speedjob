from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import JobOffer, Profile, Company

from django.core.mail import send_mail

#call this everytime a User is created (after creation = post_save)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)   #create profile for user


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):

    instance.profile.save()

@receiver(post_save, sender=Company)
def email_company(sender, instance, created, **kwargs):
    if created:
        send_mail(
                'You registered a Company!',
                f"You registered: {instance.company_name}",
                's3jobs@s3jobs.ddns.net',
                [instance.profile.user.email],
                fail_silently=False,
                )

@receiver(post_save, sender=JobOffer)
def email_company(sender, instance, created, **kwargs):
    if created:
        send_mail(
                'You registered a JobOffer!',
                f"You registered a Job Offer for: {instance.company.company_name}",
                's3jobs@s3jobs.ddns.net',
                [instance.company.profile.user.email],
                fail_silently=False,
                )