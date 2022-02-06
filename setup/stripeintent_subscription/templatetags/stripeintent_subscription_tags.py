from django import template
from django.contrib.auth.decorators import permission_required
register = template.Library()
from html import unescape
from django.utils.safestring import mark_safe
@register.simple_tag
def stripeintent_card_data(val,item,request,**kwargs):
	return_value =""
	
	if afl_keys_exists(val, "card") ==True:
		data = val['card']
		if 'brand' in  data and 'last4' in  data:
			return_value = '%(brand)s *****%(last4)s' % {'brand': data['brand'],'last4': data['last4']}
			pass
	return mark_safe(unescape(return_value))

@register.simple_tag
def stripe_live_tag(val,item,request,**kwargs):
	return_value =''
	if val ==0 or val =='0':
		return_value ="Test"
	if val ==1 or val =='1':
		return_value ="Live"
	return mark_safe(unescape(return_value))