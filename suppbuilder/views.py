from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import decimal
from allauth.account.forms import LoginForm
from allauth.account.views import *
from shopping.forms import AddressForm, GuestForm
from shopping.models import Guest, Address
from carton.cart import Cart



def IndexView(request):
	customer = request.user

	session = request.session

	current_user_id = str(request.user.id)

	if customer.is_anonymous:
		print "customer is anonymous captain here is the id"  		

	if 'email' in request.session:
		print request.session['email']
		print "deleting email captain"
		del request.session['email']
	else:
		print "no email in session captain"

	return render(request, 'suppbuilder/home.html')

 
def GuestLoginView(request):
	guest = request.user

	return render(request, 'suppbuilder/guest.html')


def StripeGuestView(request):
	
	form = AddressForm
	if request.method == 'POST':
		#create form instance from data
		guest = GuestForm(request.POST)

		if guest.is_valid():
			# guest.email= guest.cleaned_data['email
			guest, created = Guest.objects.get_or_create(
				email = guest.cleaned_data['email'],
			)			
			

		request.session['email'] = request.POST.get('email')	
	

	return render(request, 'shopping/address.html', {'form': form})






