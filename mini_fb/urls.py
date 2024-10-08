from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.ShowAllView.as_view(), name='show_all'),
]