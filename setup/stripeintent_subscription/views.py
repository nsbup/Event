from django.shortcuts import render
from django.views import View
# Create your views here.
from django.dispatch import receiver,Signal
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required,login_required
from django.http import QueryDict
from django.conf import settings
from django.forms.formsets import formset_factory
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .models import *

from django.contrib import messages
from django.forms.models import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
import traceback
from payments import get_payment_model, RedirectNeeded
from payments import FraudStatus, PaymentStatus, RedirectNeeded
import copy
import datetime
import stripe
import json

class StripePaymentIntentPublicKeyView(View):
	#@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		self.stripe = stripe
		stripe_conf = settings.PAYMENT_VARIANTS['stripeintent_subscription'][1]
		print(stripe_conf)
		self.public_key =''
		self.secret_key =''
		self.customer =''
		if stripe_conf:
			if 'public_key' in stripe_conf:
				self.public_key = stripe_conf['public_key']
		if stripe_conf:
			if 'secret_key' in stripe_conf:
				self.secret_key = stripe_conf['secret_key']
		if self.secret_key and self.public_key:
			self.stripe.api_key = self.secret_key
			
		self.order =None
		ORDER_ID=""
		self.order_id = request.session.get(ORDER_ID)
		self.data ={}
		self.user_data ={}
		self.stripesyscustomer =None
		self.save_customer_status =False
		self.payment =None
		self.customer =None
		self.cart =None
		self.transaction_object =None
		return super(StripePaymentIntentPublicKeyView, self).dispatch(request, *args, **kwargs)
	def get(self, request, *args, **kwargs):
		data ={'publicKey': self.public_key}
		
		response =  JsonResponse(data , safe=False)
		return response
	def post(self, request, *args, **kwargs):
		pp('******pay_postrequest.POSTdddd************')
		pp(request.POST)
		pp(list(request.POST)[0])
		pp(json.loads(list(request.POST)[0]))
		self.data = json.loads(list(request.POST)[0])
		cart_kwargs={
					'new_order':False
				}
		self.get_queryset()
		return self.pay_post()
		#return render(request, 'afl_commerce/afl_payment/stripe_subscription/test.html',{}) 
	def get_queryset(self):
		
		paymentModel = get_payment_model()
		self.payment = paymentModel.objects.filter(pk=int(self.data['payment_id'])).first()
	def get_amount(self):
		return int(100*100),'usd'
	
	def cart_errors_actions(self):
		if  self.cart.errors:
			message =""
			redirect_url =""
			response ={}
			for  module ,cart_module_errors in  self.cart.errors.items():
				for cart_module_error in cart_module_errors['message']:
					message = str(cart_module_error)
					response.update({
						'error':message
					})
				if 'redirect_url' in cart_module_errors:
					redirect_url =  cart_module_errors['redirect_url']
					response.update({
						'redirect_url':redirect_url
					})
			if self.order:
				self.order.order_convert_review_pending(self.cart)
			return JsonResponse(response, safe=False)
	def pay_post(self):
		pp('*****************pay_postfghghgh***************')
		try:
			
			if "paymentIntentId" not in self.data and self.payment:
				if 'cancel' in self.data and self.data['cancel']==True:
					
					return JsonResponse({'error': str('Your card was not authenticated, please try again')}, safe=False)
				else:
					
					
					amount,currency_code = self.get_amount()
					payment_intent_data = dict(
						amount=amount,
						currency=currency_code,
						payment_method=self.data['paymentMethodId'],
						confirmation_method='manual',
						confirm=True,
						metadata={
							'order_number':'test123',
						},
						#description='Email:%s' % (self.user_data['email'])
						description='Order Number: %s' % (
							'test123',
							),

						shipping = {
							"name": "Jenny Rosen",
							"address": {
							"line1": "510 Townsend St",
							"postal_code": "98140",
							"city": "San Francisco",
							"state": "CA",
							"country": "US",
							},
						},
					)
					# if self.save_customer_status:
					# 	# get or set customer using api
					# 	self.get_or_set_stripe_customer()
					# 	#if self.data['isSavingCard']:
					# 	# Create a Customer to store the PaymentMethod for reuse
						
						

					# 	payment_intent_data['customer'] = self.customer['id']
					# 	# Set save_payment_method to true to attach the PM to the Customer
					# 	payment_intent_data['save_payment_method'] = True

					# 	# setup_future_usage tells Stripe how you plan on using the saved card
					# 	# set to 'off_session' if you plan on charging the saved card when the customer is not present
					# 	payment_intent_data['setup_future_usage'] = 'off_session'

						# Create a new PaymentIntent for the order
					intent =self.stripe.PaymentIntent.create(**payment_intent_data)
			else:
				# Confirm the PaymentIntent to collect the money
				intent =self.stripe.PaymentIntent.confirm(self.data['paymentIntentId'])
				
			return self.generate_response(intent)
		except self.stripe.error.CardError as e:
			
			message =str('Some error occured.Please try again later')
			if hasattr(e,'_message'):
				message = str(e._message)
			elif hasattr(e,'error'):
				err = e.error
				traceback.print_exc()
				# The card has been declined
				return JsonResponse({'error': str(err['message'])}, safe=False)
			else:
				return JsonResponse({'error': str('Some error occured.Please try again later')}, safe=False)
			return JsonResponse({'error': message}, safe=False)
		
			
		except Exception as e:
			message =  "some error occure.Please try again later"
			if hasattr(e,'_message'):
				message = str(e._message)
			traceback.print_exc()
		
			return JsonResponse({'error':message}, safe=False)
	def generate_response(self,intent):
		status = intent['status']
		if status == 'requires_action' or status == 'requires_source_action':
			# Card requires authentication
			return JsonResponse({'requiresAction': True, 'paymentIntentId': intent['id'], 'clientSecret': intent['client_secret']}, safe=False)
		elif status == 'requires_payment_method' or status == 'requires_source':
			# Card was not properly authenticated, suggest a new payment method
			return JsonResponse({'error': 'Your card was denied, please provide a new payment method'}, safe=False)
		elif status == 'succeeded':
			# Payment is complete, authentication not required
			# To cancel the payment after capture you will need to issue a Refund (https://stripe.com/docs/api/refunds)
			pp("Pay33ment received!")
			
			
			#save customer in db
			self.save_payment(intent)
			return JsonResponse({'clientSecret': intent['client_secret']}, safe=False)
	
	def save_payment(self,intent):

		self.payment.transaction_id = intent['id']
		self.payment.attrs.charge = json.dumps(intent)
		self.payment.change_status(PaymentStatus.PREAUTH)
		
		self.payment.capture()
		# Make sure we store the info of the charge being marked as fraudulent
		self._handle_potentially_fraudulent_charge(intent)
		pass
	
	
	def _handle_potentially_fraudulent_charge(self, charge, commit=True):
		pp('******************fraudulent_charges************')
		# fraud_details = charge['fraud_details']
		# if fraud_details.get('stripe_report', None) == 'fraudulent':
		# 	self.payment.change_fraud_status(FraudStatus.REJECT, commit=commit)
		# else:
		self.payment.change_fraud_status(FraudStatus.ACCEPT, commit=commit)

'''
#######################
end check stripe intent payment
######################
'''
