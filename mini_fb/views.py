from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView

class ShowAllView(ListView):
    '''Create a subclass of ListView to display all users '''

    model = Profile
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'users'

def show_main(request):
    """ renders main.html with general info """

    # rednering the main.html template
    return render(request, 'mini_fb/main.html')