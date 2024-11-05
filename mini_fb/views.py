from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Profile, StatusMessage, Image, Friend, User
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateMessageForm, AddStatusMessageImagesForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm



class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all users '''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        '''Add user profile to the context if the user is authenticated'''
        context = super().get_context_data(**kwargs)
        
        # getting the profile associated with the logged-in user, if it exists
        if self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.filter(user_key=self.request.user).first()
        else:
            context['user_profile'] = None
        
        return context

class ShowProfilePageView(DetailView):
    ''' Create a subclass of DetailView to display user's profile '''

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'

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

        # getting the profile associated with the logged-in user, if it exists
        if self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.filter(user_key=self.request.user).first()
        else:
            context['user_profile'] = None
        
        return context

class CreateProfileView(CreateView):

    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_creation_form"] = UserCreationForm()

        return context
    
    def form_valid(self, form):
        user_creation_form = UserCreationForm(self.request.POST)

        # saving the UserCreationForm to create a new User
        user = user_creation_form.save()

        # attaching the user to the Profile instance
        form.instance.user_key = user

        # proceeding with saving the Profile by calling the superclass method
        return super().form_valid(form)


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    # passing profile information to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(Profile, user_key=self.request.user)
        context['profile'] = user_profile
        context['user_profile'] = user_profile  # Set user_profile for consistency
        return context
    
    # attaching the profile to the StatusMessage before saving
    def form_valid(self, form):
        user_profile = get_object_or_404(Profile, user_key=self.request.user)
        form.instance.profile = user_profile

        # saving the form and handle image uploads if any
        status_message = form.save()
        files = self.request.FILES.getlist('files')
        for f in files:
            new_image = Image()
            new_image.image = f
            new_image.status_message = status_message
            new_image.save()

        return super().form_valid(form)

    def get_success_url(self):
        user_profile = get_object_or_404(Profile, user_key=self.request.user)
        return reverse('show_profile', kwargs={'pk': user_profile.pk})
    
    def get_login_url(self) -> str:
        ''' returns the URL required for login '''
        return reverse('login') 
    
class UpdateProfileView(UpdateView, LoginRequiredMixin):

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self, queryset=None):
        """ retrieving the profile associated with the logged-in user """
        return get_object_or_404(Profile, user_key=self.request.user)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_object()
        return context

class DeleteStatusMessageView(DeleteView, LoginRequiredMixin):

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # getting the profile associated with the logged-in user, if it exists
        if self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.filter(user_key=self.request.user).first()
        else:
            context['user_profile'] = None
        
        return context
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):

    model = StatusMessage
    form_class = UpdateMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    def get_object(self, queryset = None):
        # Get the status message object
        status_message = super().get_object(queryset)
        
        # Check if the logged-in user is the owner of the status message
        if status_message.profile.user_key != self.request.user:
            raise PermissionDenied("You do not have permission to edit this status message.")
        
        return status_message

    def get_success_url(self):
        profile_id = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
class AddStatusMessageImages(UpdateView, LoginRequiredMixin):

    model = StatusMessage
    form_class = AddStatusMessageImagesForm
    template_name = 'mini_fb/add_status_message_images.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object

        # getting the profile associated with the logged-in user, if it exists
        if self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.filter(user_key=self.request.user).first()
        else:
            context['user_profile'] = None
        
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
    
class DeleteStatusMessageImagesView(DeleteView, LoginRequiredMixin):

    model = StatusMessage
    form_class = AddStatusMessageImagesForm
    template_name = 'mini_fb/delete_status_message_images.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['status_message'] = self.object

        # getting the profile associated with the logged-in user, if it exists
        if self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.filter(user_key=self.request.user).first()
        else:
            context['user_profile'] = None
        
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class DeleteStatusMessageImageView(DeleteView, LoginRequiredMixin):

    model = Image
    template_name = 'mini_fb/delete_status_message_image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = self.object  
        context['status_message'] = self.object.status_message

        # getting the profile associated with the logged-in user, if it exists
        if self.request.user.is_authenticated:
            context['user_profile'] = Profile.objects.filter(user_key=self.request.user).first()
        else:
            context['user_profile'] = None
        
        return context

    def get_success_url(self):
        profile_id = self.object.status_message.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_id})
    
class CreateFriendView(View, LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user_key=request.user)
        
        other_pk = self.kwargs['other_pk']
        other_profile = get_object_or_404(Profile, pk=other_pk)

        user_profile.add_friend(other_profile)

        return redirect('show_profile', pk=user_profile.pk)
    
class ShowFriendSuggestionsView(DetailView, LoginRequiredMixin):

    template_name = 'mini_fb/friend_suggestions.html'
    model = Profile
    context_object_name = 'profile'

    def get_success_url(self):
        return reverse('see_suggestions')
    
    def get_context_data(self, **kwargs):
        ''' override to have friends in groups of 5 '''

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        friend_suggestions = profile.get_friend_suggestions()

        # grouping friends into rows of 5
        friends_in_rows = [friend_suggestions[i:i + 5] for i in range(0, len(friend_suggestions), 5)]
        context['friends_in_rows'] = friends_in_rows

        context['user_profile'] = profile
        
        return context
    
    def get_object(self):
        """ overrrided to get the Profile object for the logged-in user """
        return get_object_or_404(Profile, user_key=self.request.user)
    
class ShowNewsFeedView(DetailView, LoginRequiredMixin):

    template_name = 'mini_fb/news_feed.html'
    model = Profile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """ retrieving the profile associated with the logged-in user """
        return get_object_or_404(Profile, user_key=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_object()
        return context