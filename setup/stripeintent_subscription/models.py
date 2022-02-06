from django.db import models
from django.utils import timezone
from django.contrib import admin
#from afl_core.afl_common.utilities import AflGetOptionFromList
from django.utils.text import slugify
# Create your models here.

class StripeIntentCard(models.Model):
	setup_intent = models.CharField(max_length=1000, default='', null=True,blank=True) #Stripe Payment Method
	class Meta:
		managed = False	
class StripeIntentSubscriptionOption(models.Model):
	uid = models.IntegerField(default=0, blank=True)
	class Meta:
		managed = False	

class StripeIntentPaymentCheck(models.Model):
	order_number = models.CharField(max_length=200, default='')
	
	class Meta:
		managed = False	