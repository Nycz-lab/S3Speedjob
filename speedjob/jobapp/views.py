from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.mail import send_mail

from .models import Company, Contact
from .forms import RegisterForm

from django.db.models import Q



def index(request):
    return render(request, 'jobapp/index.html')

def companies(request):
    return render(request, 'jobapp/companies.html', {'companies' : Company.objects.all()})


def company(request, id):
    try:
        contact = Contact.objects.get(company_id = id)
    except Contact.DoesNotExist:
        contact = None

    return render(request, 'jobapp/company.html', {'company' : get_object_or_404(Company, id=id),
     'contact' : contact})

def search(request):
    query = request.GET.get('q')
    if query:
        company_list = Company.objects.filter(
            Q(company_name__icontains=query)
        )
        contact_list = Contact.objects.filter(
            Q(contact_firstName__icontains=query) | Q(contact_lastName__icontains=query)
        )
        return render(request, 'jobapp/search_results.html', {'company_list' : company_list, 'contact_list' : contact_list})
    else:
        return render(request, 'jobapp/search.html')



def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            company = Company(company_name = form.cleaned_data['company_name'],
            company_description = form.cleaned_data['company_description'],
            company_address_city = form.cleaned_data['company_address_city'],
            company_address_plz = form.cleaned_data['company_address_plz'],
            company_address_street = form.cleaned_data['company_address_street'],)
            company.save()

            contact = Contact(company_id = company.id, contact_firstName = form.cleaned_data['firstName'],
            contact_lastName = form.cleaned_data['lastName'],
            contact_phone = form.cleaned_data['phone'],
            contact_email = form.cleaned_data['email'],)
            contact.save()

            # FOR SENDING MAILS LATER NEED TO CONFIGURE SMTP SERVER FIRST
            """
            send_mail(
            'Test',
            'Test2',
            'noreply@jobappS3.com',
            [contact.contact_email],
            fail_silently=True,
            )"""

            return HttpResponseRedirect(reverse('company', args=(company.id,)))



        else:
            return HttpResponse("and error occured!")
    else:
        return render(request, 'jobapp/createAppl.html', {'form': RegisterForm})
# Create your views here.
