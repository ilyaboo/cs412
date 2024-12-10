from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length = 50, 
        required = True, 
        widget = forms.TextInput(attrs = {"placeholder": "First Name"})
    )

    last_name = forms.CharField(
        max_length = 50, 
        required = True, 
        widget = forms.TextInput(attrs = {"placeholder": "Last Name"})
    )

    email = forms.EmailField(
        required = True,
        widget = forms.EmailInput(attrs = {"placeholder": "Email Address"}),
        help_text = "Will be used in case you lose access to the account."
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize placeholder text
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter a password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Re-enter your password"})

        # Optional: Remove default help_text or modify it
        self.fields["username"].help_text = "\nThis username will be seen by other users"
        self.fields["password1"].help_text = "Your password must be at least 8 characters long and contain a mix of letters, numbers, and symbols."
        self.fields["password2"].help_text = "Re-enter the same password as above."