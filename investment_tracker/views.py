from typing import Any
from django.db.models.base import Model as Model
from django.urls import reverse
from django.db.models.query import QuerySet
from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from .models import Profile, Portfolio, Asset, PurchasedAsset
from .utils.yfinance_utils import get_latest_stock_price, get_latest_crypto_price

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
    
class PortfolioPageView(DetailView):
    """ view to display information about a Portfolio """

    model = Portfolio
    template_name = "investment_tracker/portfolio_page.html"
    context_object_name = "portfolio"

    def get_context_data(self, **kwargs):
        """ passing the assets portfolio contains """

        # obtaining prices and changes
        context = super().get_context_data(**kwargs)
        portfolio_assets_objects = PurchasedAsset.objects.filter(portfolio = self.object)
        portfolio_assets_with_info = [{"portfolio_asset_object": asset,
                                       "current_price": asset.asset.get_current_price()} \
                                        for asset in portfolio_assets_objects]
        
        # obtaining changes in value
        for i in range(len(portfolio_assets_with_info)):
            current_price = portfolio_assets_with_info[i]["current_price"]
            portfolio_assets_with_info[i]["current_value"] = current_price * \
                                                            float(portfolio_assets_with_info[i]["portfolio_asset_object"].purchase_quantity)
            portfolio_assets_with_info[i]["current_value_change"] = portfolio_assets_with_info[i]["current_value"] - \
                                                                    float(portfolio_assets_with_info[i]["portfolio_asset_object"].get_initial_value())
            portfolio_assets_with_info[i]["current_value_change_percentage"] = portfolio_assets_with_info[i]["current_value_change"] / \
                                                                                float(portfolio_assets_with_info[i]["portfolio_asset_object"].get_initial_value()) * 100
            if portfolio_assets_with_info[i]["current_value_change"] >= 0:
                portfolio_assets_with_info[i]["current_value_change"] = "+$" + str(round(portfolio_assets_with_info[i]["current_value_change"], 2))
                portfolio_assets_with_info[i]["current_value_change_percentage"] = "+" + str(round(portfolio_assets_with_info[i]["current_value_change_percentage"], 2))
            else:
                portfolio_assets_with_info[i]["current_value_change"] = "-$" + str(round(portfolio_assets_with_info[i]["current_value_change"], 2))[1 : ]
                portfolio_assets_with_info[i]["current_value_change_percentage"] = str(round(portfolio_assets_with_info[i]["current_value_change_percentage"], 2))

        context["portfolio_assets_with_info"] = portfolio_assets_with_info
        
        return context
    
class AssetPageView(DetailView):
    """ view to display information about the asset """

    model = Asset
    template_name = "investment_tracker/asset_page.html"
    context_object_name = "asset"
    slug_field = "ticker"
    slug_url_kwarg = "ticker"

    def get_context_data(self, **kwargs):
        """ adding price and purchase mode information to the context """

        context = super().get_context_data(**kwargs)
        asset = self.object

        if asset.asset_type == "stock":
            context["price"] = round(get_latest_stock_price(asset.ticker), 2)
        else:
            context["price"] = round(get_latest_crypto_price(asset.ticker), 2)

        # checking if we are in purchase mode
        context["from_portfolio"] = self.request.GET.get("from_portfolio", "false") == "true"

        return context
    
class AddToPortfolioDraftView(LoginRequiredMixin, View):
    """ view to handle adding an asset to the portfolio draft """

    def post(self, request, *args, **kwargs):
        ticker = kwargs["ticker"]
        asset = Asset.objects.get(ticker = ticker)

        if asset.asset_type == "stock":
            price = get_latest_stock_price(ticker)
        else:
            price = get_latest_crypto_price(ticker)

        quantity = float(request.POST.get("quantity", 1))
        total_cost = float(request.POST.get("total_cost", float(price) * quantity))
        
        # adding the asset to the draft in the session
        draft_assets = request.session.get("draft_assets", [])

        # checking if this asset is already present in the draft
        if asset.ticker in [val["ticker"] for val in draft_assets]:
            i = [val["ticker"] for val in draft_assets].index(asset.ticker)
            draft_assets[i]["quantity"] += quantity
            draft_assets[i]["total_cost"] += quantity * draft_assets[i]["price"]
        else:    
            draft_assets.append({"ticker": asset.ticker, "name": asset.name, "price": price, "quantity": quantity, "total_cost": total_cost})
        request.session["draft_assets"] = draft_assets

        return redirect(reverse("create_portfolio"))
    
class AssetsListView(ListView):
    """ view to display all assets """

    template_name = "investment_tracker/all_assets.html"
    model = Asset
    context_object_name = "assets"
    paginate_by = 25

    def get_queryset(self):
        """ obtaining assets according to filters """

        qs = super().get_queryset().order_by("ticker")

        # filter by asset type
        asset_type_search = self.request.GET.get("asset_type")
        if asset_type_search:
            qs = qs.filter(asset_type = asset_type_search)

        # filter by name
        name_search = self.request.GET.get("name")
        if name_search:
            qs = qs.filter(name__icontains = name_search)

        # filter by tinker
        ticker_search = self.request.GET.get("ticker")
        if ticker_search:
            qs = qs.filter(ticker = ticker_search)

        # sorting
        sort_by = self.request.GET.get("sort_by")
        if sort_by == "name_asc":
            qs = qs.order_by("name")
        elif sort_by == "name_desc":
            qs = qs.order_by("-name")
        elif sort_by == "ticker_asc":
            qs = qs.order_by("ticker")
        elif sort_by == "ticker_desc":
            qs = qs.order_by("-ticker")
        else:
            qs = qs.order_by("ticker")

        return qs
    
    def get_context_data(self, **kwargs):
        """ context data to preserve search parameters """

        context = super().get_context_data(**kwargs)

        # checking/preserving from_portfolio parameter
        context["from_portfolio"] = self.request.GET.get("from_portfolio", "false") == "true"

        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        context["query_params"] = query_params.urlencode()

        return context
    
class PortfolioCreateView(LoginRequiredMixin, TemplateView):
    """ view that handles the creation of a new portfolio """

    template_name = "investment_tracker/create_portfolio.html"

    def get_context_data(self, **kwargs):
        """ pass portfolio draft assets and total cost """

        context = super().get_context_data(**kwargs)
        draft_assets = self.request.session.get("draft_assets", [])

        # extracting current asset prices
        for i in range(len(draft_assets)):
            a_obj = Asset.objects.get(ticker = draft_assets[i]["ticker"])
            draft_assets[i]["price"] = a_obj.get_current_price()
            draft_assets[i]["total_cost"] = draft_assets[i]["price"] * draft_assets[i]["quantity"]

        context["draft_assets"] = draft_assets

        context["total_cost"] = sum([asset["price"] * asset["quantity"] for asset in draft_assets])
        return context

    def post(self, request, *args, **kwargs):
        """ handles form submission to set portfolio name or finalize """

        portfolio_name = request.POST.get("portfolio_name")
        if portfolio_name:
            request.session["portfolio_name"] = portfolio_name
            return redirect("finalize_portfolio")
        return self.get(request, *args, **kwargs)
    
class ClearDraftAssetsView(LoginRequiredMixin, View):
    """ view to clear all draft assets from the session """

    def post(self, request, *args, **kwargs):
        if "draft_assets" in request.session:
            del request.session["draft_assets"]
        
        # redirecting back to the portfolio creation page
        return redirect("create_portfolio")
    
class RemoveDraftAssetView(View):
    """ view to handle the removal of an asset from the portfolio draft """

    def post(self, request, *args, **kwargs):
        ticker = kwargs["ticker"]

        # getting the current draft assets from the session
        draft_assets = request.session.get("draft_assets", [])

        draft_assets = [asset for asset in draft_assets if asset["ticker"] != ticker]
        request.session["draft_assets"] = draft_assets

        return redirect("create_portfolio")

class CreatedPortfolioView(LoginRequiredMixin, View):
    """ finalizes portfolio creation """

    template_name = "investment_tracker/created_portfolio.html"

    def get(self, request, *args, **kwargs):
        profile = request.user.investment_tracker_profiles
        portfolio_name = request.session.get("portfolio_name", "New Portfolio")
        draft_assets = request.session.get("draft_assets", [])

        # creating portfolio
        portfolio = Portfolio.objects.create(portfolio_name=portfolio_name, portfolio_owner=profile)

        # creating purchased assets
        for asset in draft_assets:
            PurchasedAsset.objects.create(
                portfolio = portfolio,
                asset = Asset.objects.get(ticker = asset["ticker"]),
                purchase_price = Asset.objects.get(ticker = asset["ticker"]).get_current_price(),
                purchase_quantity = asset["quantity"],
            )

        # clearing session
        request.session.pop("portfolio_name", None)
        request.session.pop("draft_assets", None)

        return redirect("portfolio", portfolio.slug)