from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all users '''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'users'

class ShowProfilePageView(DetailView):
    ''' Create a subclass of DetailView to display user's profile '''

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'user'

def show_main(request):
    """ renders main.html with general info """

    # rednering the main.html template
    return render(request, 'mini_fb/main.html')