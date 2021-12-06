from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

#url patterns for navigating to the python response
urlpatterns = [
    path('', views.index, name='index'),
    path('companies/', views.companies, name='companies'),
    path('companies/<int:id>/', views.company, name='company'),
    path('search/', views.search, name='search'),
    path('registerCompany/', views.registerCompany, name='registerCompany'),
    path('registerJobOffer/', views.registerJobOffer, name='registerJobOffer'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),

    path('activate/<str:uid>/<str:token>/', views.activate, name='activate'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>', views.profiles, name='profiles'),
]
