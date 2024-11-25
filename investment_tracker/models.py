from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        """ string representation of a Portfolio object """

        return f'{self.portfolio_name} ({self.portfolio_owner.first_name}\'s portfolio created at {self.portfolio_creation_time})'
    
class PurchasedAsset(models.Model):
    """ a model that corresponds to an asset purchased (added) to the portfolio """

    portfolio = models.ForeignKey(Portfolio, on_delete = models.CASCADE)
    asset_name = models.CharField(max_length = 100)
    purchase_time = models.DateTimeField(auto_now_add = True)
    purchase_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    purchase_quantity = models.DecimalField(max_digits = 10, decimal_places = 4)

    def __str__(self):
        """ string representation of the PurchasedAsset object """

        return f'{self.purchase_quantity} of {self.asset_name} purchased at the price of {self.purchase_price} for {self.portfolio.portfolio_name} by {self.portfolio.portfolio_owner.first_name}'