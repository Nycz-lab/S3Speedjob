from django.shortcuts import render, get_object_or_404, redirect                            # for rendering templates, throwing 404s and redirecting

from django.http import HttpResponse, HttpResponseRedirect                                  # for returning HttpResponse Objects
from django.urls import reverse

from django.core.mail import send_mail                                                      # for mail managing (smtp)

from .models import Company, Profile, JobOffer, Tag                                            # Database Models
from .forms import RegisterForm, UserRegistrationForm, ProfileForm, RegisterJobOfferForm    # Django Forms for given Database Models

from django.contrib.auth import login, authenticate                                         # django standard authentication methods
from django.contrib import messages                                                         # for sending messages and displaying via html

from django.db.models import Q                                                              # SQL Queries
from django.contrib.auth.models import User                                                 # predefined django user model

from django.conf import settings                                                            # mainly for checking if DEBUG mode is enabled

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

def retrieveTags(profiles):                                                         # stupid but havent found another way yet
    TagProfile = Tag.profiles.through

    staff_tags = {}
    for profile in profiles:
        staff_tags[profile] = []
        for tag_id in TagProfile.objects.filter(profile=profile).values('tag_id'):
            staff_tags[profile].append(tag_id['tag_id'])



    tag_words = {}
    for profile in staff_tags:
        tag_words[profile] = []
        for tags in range(0, len(staff_tags[profile])):
            tag_words[profile].append(Tag.objects.get(id=staff_tags[profile][tags]))


    return tag_words

def index(request):                                                                         # Index Site

    TagProfile = Tag.profiles.through


    staff_accs = User.objects.filter(is_staff=True)
    staff_profiles = Profile.objects.filter(id__in=staff_accs.values('pk'))

    tag_words = retrieveTags(staff_profiles)
    print(staff_accs)


    print(tag_words)
    return render(request, 'jobapp/index.html', {'DEBUG': settings.DEBUG,
    'users':staff_accs, 'tags': tag_words})

def companies(request):                                                                     # display all company objects
    return render(request, 'jobapp/companies.html', {'companies' : Company.objects.all()})


def company(request, id):                                                                   # display specific company object
    contact = Profile.objects.get(company = id)
    job_offers = JobOffer.objects.filter(company= id).order_by('offer_date')
    auth = False
    try:
        if(contact == request.user.profile):    #check if current user registered company
            auth = True
    except Exception:
            auth = False

    return render(request, 'jobapp/company.html', {'company' : get_object_or_404(Company, id=id),
     'contact' : contact, 'auth': auth, 'offers': job_offers})

def search(request):                                                                        # search database for specific input query
    query = request.GET.get('q')                                            # read query from url via GET http method
    if query:                                                               # if there is a query
        company_list = Company.objects.filter(
            Q(company_name__icontains=query), company_approved = True
        ).order_by('company_name')
        job_offer_list = JobOffer.objects.filter(
            Q(tag__word__icontains=query), company__company_approved = True
        ).order_by('offer_date')
        contact_list = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        ).order_by('username')
        return render(request, 'jobapp/search_results.html', {'company_list' : company_list, 'offers' : job_offer_list,'contact_list' : contact_list})
    else:
        return render(request, 'jobapp/search.html')



def registerCompany(request):                                                                # register company to database

    if request.method == "POST":    # check if data was POSTED via http to url
        form = RegisterForm(request.POST)

        if form.is_valid():         # check if form was filled correctly



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

def registerJobOffer(request):                                                              # register job offer
    if request.method == 'POST':
        form = RegisterJobOfferForm(request.POST,profile=request.user.profile)

        form.save()
        return HttpResponseRedirect(reverse('company', args=(form.cleaned_data['company'].id,)))
    else:
        form = RegisterJobOfferForm(profile=request.user.profile)
        return render(request, 'jobapp/registerJobOffer.html', {'form': form})


def register(request):                                                                      # register user
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))

            url = f"{request.get_host()}/activate/{uid}/{token}/"               # change this to support html code later!
            message = f"Nice to meet you {user.username}!\n         \
            Click the following link to activate your account!\n    \
            {url}"

            send_mail(
            'Confirm Email',
            message,
            's3jobs@s3jobs.ddns.net',
            [user.email],
            fail_silently=False,
            )

            if settings.DEBUG:
                print(f"New User: token: {token} uid: {uid}")

            messages.success(request, f'Your account has been created. Confirm your Email now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form' : form})

def activate(request, uid, token):                                      # activate account via email confirmation

    if uid and token:
        uid = urlsafe_base64_decode(uid)                    # generate url from encoded uid and user token
        user = User.objects.get(id=uid)


        if default_token_generator.check_token(user, token) and user.is_active == 0:        #check if token and uid are correct
            user.is_active = 1
            user.save()
            return render(request, 'accounts/activate.html')

        return HttpResponse("ERROR")                                    #error handling
    return HttpResponse("FATAL ERROR")


def profiles(request, username):                                                             # display profiles from db
    user_profile = User.objects.get(username = username)
    profile = Profile.objects.get(id = user_profile.id)
    companies = Company.objects.filter(profile = profile)
    return render(request, 'jobapp/profiles.html', {'user_profile' : user_profile, 'companies' : companies})


def profile(request):                                                                       # display current user profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():

            form.save()
            messages.success(request, f'Your picture has been saved!')
            return redirect('profile')
    else:
        if request.user.is_authenticated:
            form = ProfileForm(instance=request.user.profile)
            companies = Company.objects.filter(profile = request.user.profile)
            return render(request, 'jobapp/profile.html', {'form': form, 'companies': companies})
        else:
            return render(request, 'jobapp/profile.html')

# Create your views here.
