from django.views.generic import ListView
from .models import Product, Variation
from django.shortcuts import render
from carton.cart import Cart
# Create your views here.




def EnergyView(request):
	energy_products = Product.objects.all()

	caffeine = Product.objects.get(title='Caffeine')

	caffeine_variations = list(caffeine.variation_set.all())

	cart = Cart(request.session)
	
	cart_items = []

	caffeine_match = ''
	
	for item in cart.items:
		cart_items.append(item.product)

	caffeine_in_cart = [item for item in caffeine_variations if item in cart_items]

	if caffeine_in_cart:
	 	caffeine_match = caffeine_in_cart[0]

	


	context = {
		'energy_list' : energy_products,
		'caffeine' : caffeine,
		'caffeine_match' : caffeine_match,
		'caffeine_variations' : caffeine_variations
	}

	return render (request, 'products/energy.html', context)