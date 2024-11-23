from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.username

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)  # "AAPL", "Bitcoin"
    type = models.CharField(max_length=100)  # "Stock", "Crypto"
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    investments = models.ManyToManyField(Investment, related_name="portfolios")

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class HistoricalData(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.investment.name} - {self.date}"
