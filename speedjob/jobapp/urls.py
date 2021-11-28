from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

#url patterns for navigating to the python response
urlpatterns = [
    path('', views.index, name='index'),
    path('companies/', views.companies, name='companies'),
    path('companies/<int:id>/', views.company, name='company'),
    path('search/', views.search, name='search'),
    path('registerOld/', views.registerOld, name='registerOld'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='jobapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='jobapp/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
