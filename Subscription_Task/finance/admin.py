from django.contrib import admin
from .models import Customer, Subscription, Invoice

# Register your models here.

admin.site.register(Customer)
admin.site.register(Subscription)
admin.site.register(Invoice)
