from django.contrib import admin


from .models import Company, Contact, Appl, Profile
# Register your models here.

admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Appl)
admin.site.register(Profile)
