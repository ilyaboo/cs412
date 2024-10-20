from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' a form to add a Profile to the database '''

    first_name = forms.CharField(
        label="First Name", 
        max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'first name', 'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="Last Name", 
        max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'last name', 'class': 'form-control'})
    )

    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={'placeholder': 'city', 'class': 'form-control'})
    )

    email_address = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-control'})
    )

    profile_img_url = forms.URLField(
        label="Profile Image URL",
        widget=forms.URLInput(attrs={'placeholder': 'profile image URL', 'class': 'form-control'})
    )

    class Meta:
        ''' Associate this form with the Profile model '''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_img_url']

class CreateStatusMessageForm(forms.ModelForm):
    ''' a form to add a status message to the database '''

    message = forms.CharField(
        label = "Enter the Message and Attach Images", 
        max_length = 300, 
        widget = forms.TextInput(attrs={'placeholder': 'enter your message here', 'class': 'form-control'})
    )

    class Meta:
        '''associate this form with the status message model '''

        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    ''' a form to update the profile in the database '''

    class Meta:
        ''' associates this form with the Profile model '''

        model = Profile
        fields = ['city', 'email_address', 'profile_img_url']

        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'profile_img_url': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter profile image URL'})}
        
class UpdateMessageForm(forms.ModelForm):
    ''' a form to update the message in the database '''

    class Meta:
        ''' associates this form with the Profile model '''

        model = StatusMessage
        fields = ['message']

        widgets = {'message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your message'})}