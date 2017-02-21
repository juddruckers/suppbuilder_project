from django.views.generic import ListView
from .models import Product, Variation , Research
from django.shortcuts import render
from carton.cart import Cart
# Create your views here.




def EnergyView(request):

	# CART CHECK
	cart = Cart(request.session)
	cart_items = []
	for item in cart.items:
		cart_items.append(item.product)



	# CAFFEINE
	caffeine_match = ''
	caffeine = Product.objects.get(id=3)
	caffeine_products = Product.objects.all().filter(title='Caffeine')
	caffeine_research = Research.objects.all().filter(product__title='Caffeine')

	caffeine_in_cart = [item for item in caffeine_products if item in cart_items]

	if caffeine_in_cart:
	 	caffeine_match = caffeine_in_cart[0]

	#THEANINE
	theanine = Product.objects.get(id=2)
	theanine_products = Product.objects.all().filter(title='Theanine')
	theanine_match = ''

	theanine_in_cart = [item for item in theanine_products if item in cart_items]

	if theanine_in_cart:
	 	theanine_match = theanine_in_cart[0]


	context = {	
		'caffeine' : caffeine,
		'caffeine_match' : caffeine_match,
		'caffeine_products' : caffeine_products,
		'caffeine_research' : caffeine_research,
		'theanine_match' : theanine_match,
		'theanine' : theanine,
		'theanine_products' : theanine_products,
	}

	return render (request, 'products/energy.html', context)