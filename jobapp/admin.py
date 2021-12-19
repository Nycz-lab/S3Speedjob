from django.contrib import admin


from .models import Company, Tag, Profile, JobOffer
# Register your models here.

class JobOfferAdmin(admin.ModelAdmin):
    readonly_fields = ('offer_date',)

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Company)
admin.site.register(JobOffer, JobOfferAdmin)
