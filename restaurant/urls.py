from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('main/', views.show_main, name = 'main'),
    path('order/', views.make_order, name = 'order'),
    path('confirmation/', views.submit, name = 'confirmation'),
]