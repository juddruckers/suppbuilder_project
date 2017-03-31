from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import braintree
import decimal
from allauth.account.views import *
from shopping.forms import AddressForm
from shopping.models import Guest, Address
from carton.cart import Cart



def IndexView(request):
    
	template_name = 'suppbuilder/index.html'

	customer = request.user

	session = request.session

	current_user_id = str(request.user.id)

	braintree_customers = braintree.Customer.search(
		braintree.CustomerSearch.email =='juddruckers@gmail.com'
	)

	if customer.is_anonymous:
		print "customer is anonymous captain here is the id"  

	for customer in braintree_customers:
		print customer.id	


	if 'email' in request.session:
		del request.session['email']

	# result = braintree.Customer.delete("18953635")


	return render(request, 'suppbuilder/index.html')

 
def GuestLoginView(request):
	guest = request.user

	return render(request, 'suppbuilder/guest.html')


def BrainTreeCustomerView(request):

	if request.method == 'POST':
		braintree_email = request.POST.get('email')

		guest = Guest.objects.filter(email=braintree_email).first()

		if guest is None:
			result = braintree.Customer.create({
				"email" : str(braintree_email),	
			})
			
			if result.is_success == True:
				braintree_customer = result.customer
				new_guest = Guest(
					email = str(braintree_email),
					id = braintree_customer.id,
				)
				new_guest.save()

				request.session['email'] = braintree_email
				
				return render(request, 'shopping/address.html', {'form': AddressForm,})

		else:
			braintree_customer = braintree.Customer.find(str(guest.id))
			
			request.session['email'] = guest.email

			shipping_address = Address.objects.filter(email=guest.email, address_type='shipping', default_address='True').first()
			
			billing_address = Address.objects.filter(email=guest.email, address_type='shipping', default_address='True').first()
		
			if shipping_address is None:
				return render(request, 'shopping/address.html', {'form': AddressForm,})

			elif billing_address is None:
				form = BillingAddressForm(initial={'address_type': 'billing'})
				return render(request, 'shopping/billing_address.html', {'form': form})

			else:
				print "they have a billing and shipping captain"

				cart = Cart(request.session)
				
				cart_count = 0

				for product in cart.products:
				    cart_count +=1


				cart_total = cart.total + decimal.Decimal("4.99")

				token = braintree.ClientToken.generate({"customer_id": str(guest.id)})

				context = {
				    'token': token,
				    'shipping_address': shipping_address,
				    'billing_address' : billing_address,
				    'cart_count' : cart_count,
				    'cart_total' : cart_total
				}

				return render(request, 'shopping/payment_template.html', context)










