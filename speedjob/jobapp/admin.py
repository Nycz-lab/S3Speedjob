from django.contrib import admin


from .models import Company, Contact, Appl
# Register your models here.

admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Appl)
