from django.urls import path

from . import views

#url patterns for navigating to the python response
urlpatterns = [
    path('', views.index, name='index'),
    path('companies/', views.companies, name='companies'),
    path('companies/<int:id>/', views.company, name='company'),
    path('createAppl', views.createAppl, name='createAppl'),
    path('register/', views.register, name='register'),
]
