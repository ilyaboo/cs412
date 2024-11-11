from django.urls import path
from . import views

urlpatterns = [
    path('', views.VotersListView.as_view(), name = 'voters'),
    path('results', views.VotersListView.as_view(), name='results_list'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='show_voter_profile'),
]