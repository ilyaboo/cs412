from django.shortcuts import render
from django.urls import reverse
from .models import Profile, StatusMessage, Image
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.views.generic import ListView, DetailView, CreateView

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

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

class CreateProfileView(CreateView):

    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(CreateView):
    
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    # passing profile information to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # getting the profile by its pk
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile

        return context
    
    # attaching the profile to the StatusMessage before saving
    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # setting the profile of the status message
        form.instance.profile = profile

        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for f in files:
            new_image = Image()
            new_image.image = f
            new_image.status_message = sm
            new_image.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

def show_main(request):
    """ renders main.html with general info """

    # rednering the main.html template
    return render(request, 'mini_fb/main.html')