from django.views.generic import ListView
from .models import Product, Variation , Research
from django.shortcuts import render
from carton.cart import Cart
import locale
# Create your views here.




def EnergyView(request):
	locale.setlocale(locale.LC_ALL, "")
	# CART CHECK
	cart = Cart(request.session)
	cart_items = []
	for item in cart.items:
		cart_items.append(item.product)


	# CAFFEINE
	#this is the caffine for default display
	caffeine = Product.objects.get(id=1)
	print locale.currency(caffeine.price, grouping=True)
	caffeine_products = Product.objects.all().filter(title='Caffeine')
	caffeine_research = Research.objects.all().filter(product__title='Caffeine')



	caffeine_match = [item for item in caffeine_products if item in cart_items]


	#THEANINE
	theanine = Product.objects.get(id=2)
	theanine_products = Product.objects.all().filter(title='Theanine')
	theanine_research = Research.objects.all().filter(product__title='Theanine')

	theanine_match = [item for item in theanine_products if item in cart_items]




	context = {	
		'caffeine' : caffeine,
		'caffeine_match' : caffeine_match,
		'caffeine_products' : caffeine_products,
		'caffeine_research' : caffeine_research,
		'theanine_match' : theanine_match,
		'theanine' : theanine,
		'theanine_products' : theanine_products,
		'theanine_research' :theanine_research
	}

	return render (request, 'products/energy.html', context)