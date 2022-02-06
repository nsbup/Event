from __future__ import unicode_literals

from payments.forms import CreditCardPaymentForm
from payments import PaymentStatus
from collections import OrderedDict
from payments.utils import get_month_choices, get_year_choices
from payments import FraudStatus, PaymentStatus, RedirectNeeded
from django.utils.translation import ugettext as _
from payments.forms import PaymentForm as BasePaymentForm
from django import forms
RESPONSE_STATUS = {
	'1': PaymentStatus.CONFIRMED,
	'2': PaymentStatus.REJECTED}


import copy
import json
import traceback

class StripeIntentPaymentForm(BasePaymentForm):
	class Media:
		js = ['stripeintent_subscription/js/stripe_payment_intent.js',]

	payment_id = forms.CharField(widget=forms.HiddenInput())
	payment_intent = forms.CharField(widget=forms.HiddenInput(),initial=0)
	status = forms.CharField(widget=forms.HiddenInput(),initial=0)
	def __init__(self, *args, **kwargs):
		
		super(StripeIntentPaymentForm, self).__init__( hidden_inputs=False,  *args, **kwargs)
		self.template ="payment_stripe.html"
		self.init_load()
		self.assign()
		self.redirect_success_status = True
		#set fields
		self.set_field()
		if 'keyOrder' in self.fields:
			self.fields.keyOrder = self.fields_key_order
		else:
			self.fields = OrderedDict((k, self.fields[k]) for k in self.fields_key_order)
	def init_load(self):
		if self.data:
			import stripe
			self.stripe = stripe
			
			self.public_key =''
			self.secret_key =''
			self.customer =''

			self.public_key = self.provider.public_key

			self.secret_key = self.provider.secret_key
			if self.secret_key and self.public_key:
				self.stripe.api_key = self.secret_key
	def assign(self):
		self.fields_key_order =[]
	def set_field(self):
		self.fields_key_order.extend(('payment_intent','payment_id','status'))
		self.fields['payment_id'].initial = self.payment.pk
	def clean(self):
		self.cleaned_data = super(StripeIntentPaymentForm, self).clean()

		try:
			
			self.clean_new_card()
			
		except self.stripe.error.CardError as e:
			# Making sure we retrieve the charge
			err = e.error
			import traceback
			traceback.print_exc()
			
			# The card has been declined
			self._errors['__all__'] = self.error_class([str(err['message'])])
			
			self.payment.change_status(PaymentStatus.ERROR, str(err['message']))
		except Exception as e:
			#log the message
			import traceback
			traceback.print_exc()
			logger_error.error(e)
			self._errors['__all__'] = self.error_class([str(e)])
		

		return self.cleaned_data
	def clean_new_card(self):
		self.stripe_retrieve = self.stripe.PaymentIntent.retrieve(
					self.cleaned_data['payment_intent'],
				)
		if (self.stripe_retrieve
			and
			'order_number' in self.stripe_retrieve['metadata'] 
			and 
			self.cart
			and
			self.stripe_retrieve['metadata']['order_number'] ==str(self.order.order_number)
		):
			pass
		else:

			self.redirect_success_status ==False
	def get_amount(self):
		
		return int(self.payment.total*100),self.payment.currency.lower()
	
	def save(self):
		self.payment.transaction_id = self.stripe_retrieve['id']
		self.payment.attrs.charge = self.stripe_retrieve
		self.payment.change_status(PaymentStatus.PREAUTH)
		if self.provider._capture:
			self.payment.capture()
		# Make sure we store the info of the charge being marked as fraudulent
		self._handle_potentially_fraudulent_charge(self.stripe_retrieve)

	def _handle_potentially_fraudulent_charge(self, charge, commit=True):
		# fraud_details = charge['fraud_details']
		# if fraud_details.get('stripe_report', None) == 'fraudulent':
		# 	self.payment.change_fraud_status(FraudStatus.REJECT, commit=commit)
		# else:
			self.payment.change_fraud_status(FraudStatus.ACCEPT, commit=commit)

	
