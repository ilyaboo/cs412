from django.contrib import admin
from .models import User, Investment, Portfolio, HistoricalData

admin.site.register(User)
admin.site.register(Investment)
admin.site.register(Portfolio)
admin.site.register(HistoricalData)