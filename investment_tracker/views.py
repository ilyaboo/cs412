from typing import Any
from django.db.models.base import Model as Model
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from .models import Profile, Portfolio, Asset, PurchasedAsset
from .forms import CustomUserCreationForm
from .utils.yfinance_utils import get_historical_prices
from .utils.data_processing_utils import get_historical_total_values
import pandas as pd

class ShowMainPageView(ListView):
    """ view to display the main page """

    model = Profile
    template_name = "investment_tracker/main_page.html"
    context_object_name = "profiles"

    def get_context_data(self, **kwargs):
        """ context data to pass portfolios """

        context = super().get_context_data(**kwargs)
        context["all_portfolios"] = sorted(list(Portfolio.objects.all()), key = lambda x: x.get_portfolio_value_change_percentage_raw(), reverse = True)
        return context

class MyProfilePageView(LoginRequiredMixin, DetailView):
    """ view to display logged-in user's profile """

    model = Profile
    template_name = "investment_tracker/my_profile_page.html"
    context_object_name = "profile"

    def get_object(self):
        """ getting the profile of the currently logged-in user """

        return get_object_or_404(Profile, user = self.request.user)
    
class RegisterView(View):
    """ view for user registration """

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "investment_tracker/register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # saving first and last name to the Profile
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")

            Profile.objects.create(user = user, first_name = first_name, last_name = last_name)

            return redirect("login") 
        return render(request, "investment_tracker/register.html", {"form": form})
    
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
            if portfolio_assets_with_info[i]["current_value_change"] >= 0 or round(portfolio_assets_with_info[i]["current_value_change"], 2) == 0:
                portfolio_assets_with_info[i]["current_value_change"] = abs(portfolio_assets_with_info[i]["current_value_change"])
                portfolio_assets_with_info[i]["current_value_change_percentage"] = abs(portfolio_assets_with_info[i]["current_value_change_percentage"])
                portfolio_assets_with_info[i]["current_value_change"] = f'+${format(portfolio_assets_with_info[i]["current_value_change"], '.2f')}'
                portfolio_assets_with_info[i]["current_value_change_percentage"] = f'+{format(portfolio_assets_with_info[i]["current_value_change_percentage"], '.2f')}%'
            else:
                portfolio_assets_with_info[i]["current_value_change"] = f'-${format(portfolio_assets_with_info[i]["current_value_change"], '.2f')[1 : ]}'
                portfolio_assets_with_info[i]["current_value_change_percentage"] = f'{format(portfolio_assets_with_info[i]["current_value_change_percentage"], '.2f')}%'

        context["portfolio_assets_with_info"] = portfolio_assets_with_info
        context["portfolio_assets_with_info"].sort(key = lambda x: x["current_value"], reverse = True)


        # obtaining and processing data for graphs

        day_historical_total_values = get_historical_total_values(portfolio_assets_objects, "1d", "5m")
        context["day_historical_prices"] = day_historical_total_values.to_json(date_format = "iso")

        five_days_historical_total_values = get_historical_total_values(portfolio_assets_objects, "5d", "30m")
        context["five_days_historical_prices"] = five_days_historical_total_values.to_json(date_format = "iso")

        month_historical_total_values = get_historical_total_values(portfolio_assets_objects, "1mo", "1h")
        context["month_historical_prices"] = month_historical_total_values.to_json(date_format = "iso")

        three_months_historical_total_values = get_historical_total_values(portfolio_assets_objects, "3mo", "1d")
        context["three_months_historical_prices"] = three_months_historical_total_values.to_json(date_format = "iso")

        six_months_historical_total_values = get_historical_total_values(portfolio_assets_objects, "6mo", "1d")
        context["six_months_historical_prices"] = six_months_historical_total_values.to_json(date_format = "iso")

        year_historical_total_values = get_historical_total_values(portfolio_assets_objects, "1y", "1wk")
        context["year_historical_prices"] = year_historical_total_values.to_json(date_format = "iso")

        two_years_historical_total_values = get_historical_total_values(portfolio_assets_objects, "2y", "1wk")
        context["two_years_historical_prices"] = two_years_historical_total_values.to_json(date_format = "iso")

        five_years_historical_total_values = get_historical_total_values(portfolio_assets_objects, "5y", "1mo")
        context["five_years_historical_prices"] = five_years_historical_total_values.to_json(date_format = "iso")
        
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

        context["price"] = round(asset.get_current_price(), 2)

        # obtaining historical data for graph for different time periods and intervals

        day_historical_prices = get_historical_prices(asset.ticker, period = "1d", interval = "5m", type = asset.asset_type)
        context["day_historical_prices"] = day_historical_prices.to_json(date_format = "iso")

        five_days_historical_prices = get_historical_prices(asset.ticker, period = "5d", interval = "30m", type = asset.asset_type)
        context["five_days_historical_prices"] = five_days_historical_prices.to_json(date_format = "iso")

        month_historical_prices = get_historical_prices(asset.ticker, period = "1mo", interval = "1h", type = asset.asset_type)
        context["month_historical_prices"] = month_historical_prices.to_json(date_format = "iso")

        three_months_historical_prices = get_historical_prices(asset.ticker, period = "3mo", interval = "1d", type = asset.asset_type)
        context["three_months_historical_prices"] = three_months_historical_prices.to_json(date_format = "iso")

        six_months_historical_prices = get_historical_prices(asset.ticker, period = "6mo", interval = "1d", type = asset.asset_type)
        context["six_months_historical_prices"] = six_months_historical_prices.to_json(date_format = "iso")

        year_historical_prices = get_historical_prices(asset.ticker, period = "1y", interval = "1wk", type = asset.asset_type)
        context["year_historical_prices"] = year_historical_prices.to_json(date_format = "iso")

        two_years_historical_prices = get_historical_prices(asset.ticker, period = "2y", interval = "1wk", type = asset.asset_type)
        context["two_years_historical_prices"] = two_years_historical_prices.to_json(date_format = "iso")

        five_years_historical_prices = get_historical_prices(asset.ticker, period = "5y", interval = "1mo", type = asset.asset_type)
        context["five_years_historical_prices"] = five_years_historical_prices.to_json(date_format = "iso")

        # checking if we are in purchase mode
        context["from_portfolio"] = self.request.GET.get("from_portfolio", "false") == "true"

        return context
    
class AddToPortfolioDraftView(LoginRequiredMixin, View):
    """ view to handle adding an asset to the portfolio draft """

    def post(self, request, *args, **kwargs):
        ticker = kwargs["ticker"]
        asset = Asset.objects.get(ticker = ticker)

        price = asset.get_current_price()
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
    
class EditDraftAssetView(LoginRequiredMixin, TemplateView):
    """ view to handle editing an asset in the portfolio draft """

    template_name = "investment_tracker/edit_draft_asset.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticker = kwargs["ticker"]

        # getting the asset details
        asset = Asset.objects.get(ticker = ticker)
        draft_assets = self.request.session.get("draft_assets", [])
        draft_asset = next((item for item in draft_assets if item["ticker"] == ticker), None)

        context["asset"] = asset
        context["price"] = round(asset.get_current_price(), 2)

        if draft_asset:
            context["quantity"] = draft_asset["quantity"]
            context["total_cost"] = draft_asset["quantity"] * context["price"]
        else:
            # in case draft was never created
            context["quantity"] = 1
            context["total_cost"] = asset.get_current_price()

        return context

    def post(self, request, *args, **kwargs):
        ticker = kwargs["ticker"]
        asset = Asset.objects.get(ticker = ticker)

        quantity = float(request.POST.get("quantity", 1))
        total_cost = float(request.POST.get("total_cost", asset.get_current_price() * quantity))

        # updating the asset in the draft
        draft_assets = request.session.get("draft_assets", [])
        for draft_asset in draft_assets:
            if draft_asset["ticker"] == ticker:
                draft_asset["quantity"] = quantity
                draft_asset["total_cost"] = total_cost
                break

        request.session["draft_assets"] = draft_assets
        return redirect(reverse("create_portfolio"))
    
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