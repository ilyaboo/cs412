from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.ShowMainPageView.as_view(), name = "main_page"),
    path("login/", LoginView.as_view(template_name = "investment_tracker/login.html"), name = "login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path("my_profile/", views.MyProfilePageView.as_view(), name = "my_profile"),
    path("my_portfolios/", views.MyPortfoliosPageView.as_view(), name = "my_portfolios"),
]