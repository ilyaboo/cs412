from django.db import models
from django.contrib.auth.models import User
import uuid
from .utils.yfinance_utils import get_latest_stock_price, get_latest_crypto_price

class Profile(models.Model):
    """ extended version of the built-in User model """

    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = "investment_tracker_profiles")
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)

    def __str__(self):
        """ srting representation of a Profile object """

        return f'{self.user.username}'
    
class Portfolio(models.Model):
    """ a model which corresponds to a user created portfolio of assets """

    portfolio_name = models.CharField(max_length = 100, default = "My Portfolio")
    portfolio_creation_time = models.DateTimeField(auto_now_add = True)
    portfolio_owner = models.ForeignKey(Profile, on_delete = models.CASCADE)
    slug = models.UUIDField(default = uuid.uuid4, unique = True) # unique public key

    def __str__(self):
        """ string representation of a Portfolio object """

        return f'{self.portfolio_name} ({self.portfolio_owner.first_name}\'s portfolio created at {self.portfolio_creation_time})'
    
    def get_current_portfolio_value(self) -> float:
        """ returns current value of the portfolio in USD """

        portfolio_assets = PurchasedAsset.objects.filter(portfolio = self)
        total_value = 0
        for portfolio_asset in portfolio_assets:
            total_value += float(portfolio_asset.asset.get_current_price()) * float(portfolio_asset.purchase_quantity)
        return total_value
    
    def get_money_invested_in_portfolio(self) -> float:
        """ return total amount of money invested in portfolio in USD """

        portfolio_assets = PurchasedAsset.objects.filter(portfolio = self)
        total_value = 0
        for portfolio_asset in portfolio_assets:
            total_value += float(portfolio_asset.purchase_price) * float(portfolio_asset.purchase_quantity)
        return total_value
    
    def get_portfolio_value_change(self) -> str:
        """ method that calculates the absolute value change of portfolio in USD and formats it """

        change = self.get_current_portfolio_value() - self.get_money_invested_in_portfolio()
        if change >= 0 or round(change, 2) == 0:
            change = abs(change)
            return f'+${format(change, '.2f')}'
        else:
            return f'-${format(change, '.2f')[1 : ]}'
        
    def get_portfolio_value_change_percentage(self) -> str:
        """ method that calculates the value change of portfolio in % and formats it """

        change = (self.get_current_portfolio_value() - self.get_money_invested_in_portfolio()) / self.get_money_invested_in_portfolio() * 100
        change_value = self.get_current_portfolio_value() - self.get_money_invested_in_portfolio()
        if change >= 0 or round(change_value, 2) == 0:
            change = abs(change)
            return f'+{format(change, '.2f')}%'
        else:
            return f'{format(change, '.2f')}%'
    
    def get_portfolio_value_change_percentage_raw(self) -> float:
        """ method that calculates the  value change of portfolio in % and returns as float """

        return (self.get_current_portfolio_value() - self.get_money_invested_in_portfolio()) / self.get_money_invested_in_portfolio() * 100

class Asset(models.Model):
    """ a model that corresponds to a purchasable stock/crypto asset """

    ASSET_TYPE_CHOICES = [("stock", "Stock"), ("crypto", "Cryptocurrency")]

    name = models.CharField(max_length = 150)
    ticker = models.CharField(max_length = 10)
    asset_type = models.CharField(max_length = 15, choices = ASSET_TYPE_CHOICES, default = "stock")

    def __str__(self):
        """ string representation of a purchasable asset """
        
        return f'{self.ticker} - {self.name} ({self.asset_type})'
    
    def get_current_price(self):
        """ function which returns the current price of the asset """

        if self.asset_type == "stock":
            return get_latest_stock_price(self.ticker)
        else:
            return get_latest_crypto_price(self.ticker)
    
class PurchasedAsset(models.Model):
    """ a model that corresponds to an asset purchased (added) to the portfolio """

    portfolio = models.ForeignKey(Portfolio, on_delete = models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete = models.CASCADE)
    purchase_time = models.DateTimeField(auto_now_add = True)
    purchase_price = models.DecimalField(max_digits = 10, decimal_places = 4)
    purchase_quantity = models.DecimalField(max_digits = 10, decimal_places = 4)

    def __str__(self):
        """ string representation of the PurchasedAsset object """

        return f'{self.purchase_quantity} of {self.asset.ticker} purchased at the price of {self.purchase_price} for {self.portfolio.portfolio_name} by {self.portfolio.portfolio_owner.first_name}'
    
    def get_formatted_purchase_quantity(self) -> str:
        """ function that truncates decimals and returns formatted purchase quantity """

        return str(self.purchase_quantity).rstrip('0').rstrip('.')
    
    def get_initial_value(self) -> float:
        """ return initial value of the asset when it was purchased """

        return self.purchase_price * self.purchase_quantity

def load_data():
    """ function to load data records from CSV file into Django model instances """

    # delete existing records to prevent duplicates
    Asset.objects.all().delete()
    
    # loading stocks
    f = open("investment_tracker/data/stocks_tickers.csv")
    for line in f:
        ticker, name = line.split(';')
        new_asset = Asset(name = name, ticker = ticker, asset_type = "stock")
        new_asset.save()
        print(f'Created stock: {new_asset}')
    f.close()

    # loading crypto
    f = open("investment_tracker/data/crypto_tickers.csv")
    for line in f:
        ticker, name = line.split(';')
        new_asset = Asset(name = name, ticker = ticker, asset_type = "crypto")
        new_asset.save()
        print(f'Created crypto: {new_asset}')
    f.close()

    print(f'Done. Created {len(Asset.objects.all())} assets.')
