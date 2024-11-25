from typing import Any
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Profile, Portfolio

class ShowMainPageView(ListView):
    """ view to display the main page """

    model = Profile
    template_name = "investment_tracker/main_page.html"
    context_object_name = "profiles"

class MyProfilePageView(LoginRequiredMixin, DetailView):
    """ view to display logged-in user's profile """

    model = Profile
    template_name = "investment_tracker/my_profile_page.html"
    context_object_name = "profile"

    def get_object(self):
        """ getting the profile of the currently logged-in user """

        return get_object_or_404(Profile, user = self.request.user)
    
class MyPortfoliosPageView(LoginRequiredMixin, DetailView):
    """ view to display user's profile """

    model = Profile
    template_name = "investment_tracker/my_portfolios_page.html"
    context_object_name = "profile"

    def get_object(self):
        """ getting the profile of the currently logged-in user """

        return get_object_or_404(Profile, user = self.request.user)
    
    def get_context_data(self, **kwargs):
        """ adding user's portfolios to context """

        context = super().get_context_data(**kwargs)
        context["user_portfolios"] = Portfolio.objects.filter(portfolio_owner = self.get_object())
        return context
