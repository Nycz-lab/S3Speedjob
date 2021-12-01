from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.mail import send_mail

from .models import Company, Profile, JobOffer
from .forms import RegisterForm, UserRegistrationForm, ProfileForm, RegisterJobOfferForm

from django.contrib.auth import login, authenticate
from django.contrib import messages

from django.db.models import Q
from django.contrib.auth.models import User


def index(request):
    return render(request, 'jobapp/index.html')

def companies(request):
    return render(request, 'jobapp/companies.html', {'companies' : Company.objects.all()})


def company(request, id):
    contact = Profile.objects.get(company = id)
    job_offers = JobOffer.objects.filter(company= id).order_by('offer_date')
    auth = False
    try:
        if(contact == request.user.profile):
            auth = True
    except Exception:
            auth = False

    return render(request, 'jobapp/company.html', {'company' : get_object_or_404(Company, id=id),
     'contact' : contact, 'auth': auth, 'offers': job_offers})

def search(request):
    query = request.GET.get('q')
    if query:
        company_list = Company.objects.filter(
            Q(company_name__icontains=query) & Q(company_approved__icontains = True)
        ).order_by('company_name')
        job_offer_list = JobOffer.objects.filter(
            Q(tag__word__icontains=query), company__company_approved = True
        ).order_by('offer_date')
        contact_list = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).order_by('username')
        print(contact_list)
        return render(request, 'jobapp/search_results.html', {'company_list' : company_list, 'offers' : job_offer_list,'contact_list' : contact_list})
    else:
        return render(request, 'jobapp/search.html')



def registerCompany(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():



            company = Company(profile = request.user.profile,
            company_name = form.cleaned_data['company_name'],
            company_description = form.cleaned_data['company_description'],
            company_address_city = form.cleaned_data['company_address_city'],
            company_address_plz = form.cleaned_data['company_address_plz'],
            company_address_street = form.cleaned_data['company_address_street'],)
            company.save()


            return HttpResponseRedirect(reverse('company', args=(company.id,)))



        else:
            return HttpResponse("an error occured!")
    else:
        return render(request, 'jobapp/registerCompany.html', {'form': RegisterForm})

def registerJobOffer(request):
    if request.method == 'POST':
        form = RegisterJobOfferForm(request.POST,profile=request.user.profile)

        form.save()
        return HttpResponseRedirect(reverse('company', args=(form.cleaned_data['company'].id,)))
    else:
        form = RegisterJobOfferForm(profile=request.user.profile)
        return render(request, 'jobapp/registerJobOffer.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'jobapp/register.html', {'form' : form})

def profiles(request, username):
    user_profile = User.objects.get(username = username)
    profile = Profile.objects.get(id = user_profile.id)
    companies = Company.objects.filter(profile = profile)
    return render(request, 'jobapp/profiles.html', {'user_profile' : user_profile, 'companies' : companies})


def profile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():

            form.save()
            messages.success(request, f'Your picture has been saved!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
        companies = Company.objects.filter(profile = request.user.profile)
        return render(request, 'jobapp/profile.html', {'form': form, 'companies': companies})

# Create your views here.
