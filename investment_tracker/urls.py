from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.ShowMainPageView.as_view(), name = "main_page"),
    path("login/", LoginView.as_view(template_name = "investment_tracker/login.html"), name = "login"),
    path("logout/", LogoutView.as_view(), name = "logout"),
    path("my_profile/", views.MyProfilePageView.as_view(), name = "my_profile"),
    path("my_portfolios/", views.MyPortfoliosPageView.as_view(), name = "my_portfolios"),
    path("portfolio/<uuid:slug>/", views.PortfolioPageView.as_view(), name = "portfolio"),
    path("asset/<str:ticker>/", views.AssetPageView.as_view(), name = "asset_info"),
    path("assets/", views.AssetsListView.as_view(), name = "all_assets"),
    path("create_portfolio/", views.PortfolioCreateView.as_view(), name = "create_portfolio"),
    path("created_portfolio/", views.CreatedPortfolioView.as_view(), name = "finalize_portfolio"),
    path("clear_draft_assets/", views.ClearDraftAssetsView.as_view(), name = "clear_draft_assets"),
    path("add_to_draft/<str:ticker>/", views.AddToPortfolioDraftView.as_view(), name = "add_to_draft"),
    path("remove_draft_asset/<str:ticker>/", views.RemoveDraftAssetView.as_view(), name = "remove_draft_asset"),
]