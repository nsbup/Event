from django.db import models
from decimal import Decimal


# Create your models here.
# class User(models.Model):
#     uid = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     email = models.CharField(max_length=40)
#     gender = models.CharField(max_length=6)
#     password = models.CharField(max_length=20)

class Admin(models.Model):
    aid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=20)

class Event(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField()




from decimal import Decimal

from payments import PurchasedItem
from payments.models import BasePayment

class Payment(BasePayment):

    def get_failure_url(self):
        return 'http://localhost:8000/failure/'

    def get_success_url(self):
        return 'http://localhost:8000/success/'

    def get_purchased_items(self):
        # you'll probably want to retrieve these from an associated order
        yield PurchasedItem(name='The Hound of the Baskervilles', sku='BSKV',
                            quantity=9, price=Decimal(10), currency='USD')
