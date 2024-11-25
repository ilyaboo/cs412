from django.contrib import admin
from .models import Profile, Portfolio, PurchasedAsset

admin.site.register(Profile)
admin.site.register(Portfolio)
admin.site.register(PurchasedAsset)