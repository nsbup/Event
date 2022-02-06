from django.conf.urls import url
from django.urls import path
from . import views as stripeintent_subscription
app_name = 'stripeintent_subscription'

urlpatterns = [


	path('stripe-intent/intent/publickey/', stripeintent_subscription.StripePaymentIntentPublicKeyView.as_view(), name='public_key')
]