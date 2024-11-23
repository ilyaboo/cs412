from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('investments/', views.InvestmentListView.as_view(), name='investment_list'),
    path('portfolio/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio_detail'),
]