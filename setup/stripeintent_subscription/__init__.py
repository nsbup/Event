from __future__ import unicode_literals
from decimal import Decimal
import json

import stripe

from .forms import StripeIntentPaymentForm
from payments import RedirectNeeded, PaymentError, PaymentStatus
from payments.core import BasicProvider

class StripeIntentSubscriptionProvider(BasicProvider):

	form_class = StripeIntentPaymentForm
	
	def __init__(self,public_key, secret_key, **kwargs):
		
		stripe.api_key = secret_key
		self.secret_key = secret_key
		self.public_key = public_key
		super(StripeIntentSubscriptionProvider, self).__init__(**kwargs)

	def get_form(self, payment, data=None):
		if payment.status == PaymentStatus.WAITING:
			payment.change_status(PaymentStatus.INPUT)
		form = self.form_class(
			data=data, payment=payment, provider=self)
		
		if form.is_valid():
			form.save()
			if form.redirect_success_status ==True:
				raise RedirectNeeded(payment.get_success_url())
			else:
				raise RedirectNeeded(payment.get_failure_url())
		if form.redirect_success_status ==False:    
			raise RedirectNeeded(payment.get_failure_url())
		return form

	def capture(self, payment, amount=None):
		amount = (amount or payment.total)
		
		
		# payment.attrs.capture = json.dumps(charge)
		return amount