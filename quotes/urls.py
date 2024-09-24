from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.base, name = 'base'),
    path('quote/', views.quote, name = 'random_quote'),
    path('show_all/', views.show_all, name = 'show_all'),
    path('about/', views.about, name = 'about'),
    path('form/', views.show_form, name = 'show_form'),
    path('submit/', views.submit, name = 'submit'),
]