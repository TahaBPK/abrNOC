from django.db import models
from django.contrib.auth.models import User
import time


# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=100)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, primary_key=True)
    cost = models.IntegerField()
    is_active = models.BooleanField(default=True)
    start_time = models.BigIntegerField(default=round(time.time()))
    stop_timer = models.BigIntegerField(default=round(time.time()))

    def __str__(self):
        return self.name


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    subscription_type = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    start_date = models.BigIntegerField()
    end_date = models.BigIntegerField()

    def __str__(self):
        return str(self.id)
