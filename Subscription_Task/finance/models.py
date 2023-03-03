from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.IntegerField()

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, primary_key=True)
    cost = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    price = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.id)
