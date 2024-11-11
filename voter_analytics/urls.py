from django.urls import path
from . import views

urlpatterns = [
    path('', views.VotersListView.as_view(), name = 'voters'),
    path('results', views.VotersListView.as_view(), name='results_list'),    
]