from django.views.generic import ListView, DetailView
from .models import User, Investment, Portfolio

class UserListView(ListView):
    model = User
    template_name = 'investment_tracker/user_list.html'
    context_object_name = 'users'

class InvestmentListView(ListView):
    model = Investment
    template_name = 'investment_tracker/investment_list.html'
    context_object_name = 'investments'

class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'investment_tracker/portfolio_detail.html'
    context_object_name = 'portfolio'