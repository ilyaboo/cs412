from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Profile, StatusMessage, Image, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateMessageForm, AddStatusMessageImagesForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View

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
    
    def get_context_data(self, **kwargs):
        ''' override to have friends in groups of 5 '''

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        friends = profile.get_friends()

        # grouping friends into rows of 5
        friends_in_rows = [friends[i:i + 5] for i in range(0, len(friends), 5)]
        context['friends_in_rows'] = friends_in_rows
        
        return context

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
    
class UpdateProfileView(UpdateView):

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

class DeleteStatusMessageView(DeleteView):

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
class UpdateStatusMessageView(UpdateView):

    model = StatusMessage
    form_class = UpdateMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
class AddStatusMessageImages(UpdateView):

    model = StatusMessage
    form_class = AddStatusMessageImagesForm
    template_name = 'mini_fb/add_status_message_images.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object

        return context
    
    def form_valid(self, form):

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
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class DeleteStatusMessageImagesView(DeleteView):

    model = StatusMessage
    form_class = AddStatusMessageImagesForm
    template_name = 'mini_fb/delete_status_message_images.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object

        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class DeleteStatusMessageImageView(DeleteView):

    model = Image
    template_name = 'mini_fb/delete_status_message_image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = self.object  
        context['status_message'] = self.object.status_message
        return context

    def get_success_url(self):
        profile_id = self.object.status_message.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
class CreateFriendView(View):

    def dispatch(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']

        profile = list(Profile.objects.filter(pk = pk))[0]
        other_profile = list(Profile.objects.filter(pk = other_pk))[0]

        profile.add_friend(other_profile)

        # Redirect back to the profile page of the current user
        return redirect('show_profile', pk=pk)
    
class ShowFriendSuggestionsView(DetailView):

    template_name = 'mini_fb/friend_suggestions.html'
    model = Profile
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        ''' override to have friends in groups of 5 '''

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        friend_suggestions = profile.get_friend_suggestions()

        # grouping friends into rows of 5
        friends_in_rows = [friend_suggestions[i:i + 5] for i in range(0, len(friend_suggestions), 5)]
        context['friends_in_rows'] = friends_in_rows
        
        return context
    
class ShowNewsFeedView(DetailView):

    template_name = 'mini_fb/news_feed.html'
    model = Profile
    context_object_name = 'user'

    
def show_main(request):
    """ renders main.html with general info """

    # rednering the main.html template
    return render(request, 'mini_fb/main.html')