from django.views.generic import ListView
from .models import Product, Variation , Research
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from carton.cart import Cart
import locale
# Create your views here.

def ProteinCount(request):
	cart = Cart(request.session)

	# if the item is a category of protein
	protein_count = 0
	for product in cart.items:
		if 'Protein' in product.product.title:
			serving = product.product.serving_size
			serving_number = [int(s) for s in serving.split() if s.isdigit()]
			protein_count = protein_count + serving_number[0]
			print protein_count
		
	return HttpResponse(protein_count)
	

def EnergyView(request):
	locale.setlocale(locale.LC_ALL, "")

	"""
	This view will first check if any of the products exist in the session cart

	cart_items will contain the name of the product (string)

	variation_list will contain the ID's of the variations that 
	have already been added to the cart.
	
	"""
	cart = Cart(request.session)
	cart_items = []
	variation_list = []

	"""
	for each already added item add the product name into the
	cart items list and the variation id into the variation_list
	"""
	for item in cart.items:
		variation_list.append(item.product.id)
		cart_items.append(str(item.product.product.title))

	# retreive all products to be displayed on the products page.
	products = Product.objects.all()

	context = {

		"products" :products, 
		"cart": cart, 
		"cart_items": cart_items, 
		"variation_list": variation_list
	}

	print variation_list

	return render (request, 'products/energy.html', context)


def VitaminView(request):

	# CART CHECK
	cart = Cart(request.session)
	cart_items = []
	for item in cart.items:
		cart_items.append(item.product)


	vitamin_c = Product.objects.get(id=5)
	vitamin_c_products = Product.objects.all().filter(title='Vitamin C')
	vitamin_c_research = Research.objects.all().filter(product__title='Vitamin C')
	vitamin_c_match = [item for item in vitamin_c_products if item in cart_items]





	vitamin_d = Product.objects.get(id=8)
	vitamin_d_products = Product.objects.all().filter(title='Vitamin D')
	vitamin_d_research = Research.objects.all().filter(product__title='Vitamin D')
	vitamin_d_match = [item for item in vitamin_d_products if item in cart_items]


	fish_oil = Product.objects.get(id=32)
	fish_oil_products = Product.objects.all().filter(title='Fish Oil')
	fish_oil_research = Research.objects.all().filter(product__title='Fish O3il')
	fish_oil_match = [item for item in fish_oil_products if item in cart_items]

	glucosamine = Product.objects.get(id=38)
	glucosamine_products = Product.objects.all().filter(title='Glucosamine')
	glucosamine_research = Research.objects.all().filter(product__title='Glucosamine')
	glucosamine_match = [item for item in glucosamine_products if item in cart_items]



	context = {	
		'vitamin_d_match' : vitamin_d_match,
		'vitamin_d' : vitamin_d,
		'vitamin_d_products' : vitamin_d_products,
		'vitamin_d_research' : vitamin_d_research,
		'vitamin_c_match' : vitamin_c_match,
		'vitamin_c' : vitamin_c,
		'vitamin_c_products' : vitamin_c_products,
		'vitamin_c_research' : vitamin_c_research,
		'fish_oil_match' : fish_oil_match,
		'fish_oil' : fish_oil,
		'fish_oil_products' : fish_oil_products,
		'fish_oil_research' : fish_oil_research,
		'glucosamine_match' : glucosamine_match,
		'glucosamine' : glucosamine,
		'glucosamine_products' : glucosamine_products,
		'glucosamine_research' : glucosamine_research
	}

	return render (request, 'products/vitamin.html', context)




def ProteinView(request):

	# CART CHECK
	cart = Cart(request.session)
	cart_items = []
	for item in cart.items:
		cart_items.append(item.product)

	protein_count = 0
	for product in cart.items:
		if 'Protein' in product.product.title:
			serving = product.product.serving_size
			serving_number = [int(s) for s in serving.split() if s.isdigit()]
			protein_count = protein_count + serving_number[0]
			print protein_count

	whey = Product.objects.get(id=10)
	# print locale.currency(caffeine.price, grouping=True)
	whey_products = Product.objects.all().filter(title='Whey Protein')
	whey_research = Research.objects.all().filter(product__title='Whey Protein')

	whey_match = [item for item in whey_products if item in cart_items]

	#THEANINE
	caseine = Product.objects.get(id=11)
	caseine_products = Product.objects.all().filter(title='Caseine Protein')
	caseine_research = Research.objects.all().filter(product__title='Theanine')

	caseine_match = [item for item in caseine_products if item in cart_items]

	pea_protein = Product.objects.get(id=39)
	pea_protein_products = Product.objects.all().filter(title='Pea Protein')
	pea_protein_research = Research.objects.all().filter(product__title='Pea Protein')
	pea_protein_match = [item for item in pea_protein_products if item in cart_items]

	soy_protein = Product.objects.get(id=44)
	soy_protein_products = Product.objects.all().filter(title='Soy Protein')
	soy_protein_research = Research.objects.all().filter(product__title='Soy Protein')
	soy_protein_match = [item for item in soy_protein_products if item in cart_items]


	context = {	
		'whey' : whey,
		'whey_research' : whey_research,
		'whey_products' : whey_products,
		'whey_match' : whey_match,
		'whey_research': whey_research,
		'caseine_match' : caseine_match,
		'caseine' : caseine,
		'caseine_products' : caseine_products,
		'caseine_research' : caseine_research,
		'pea_protein_match' : pea_protein_match,
		'pea_protein' : pea_protein,
		'pea_protein_products' : pea_protein_products,
		'pea_protein_research' : pea_protein_research,
		'soy_protein_match' : soy_protein_match,
		'soy_protein' : soy_protein,
		'soy_protein_products' : soy_protein_products,
		'soy_protein_research' : soy_protein_research,
		'protein_count' : protein_count
	}

	return render (request, 'products/protein.html', context)



def NewProteinView(request):

	cart = Cart(request.session)
	cart_2 = Cart(request.session, session_key='CART-2')
	cart_3 = Cart(request.session, session_key='CART-3')
	cart_4 = Cart(request.session, session_key='CART-4')
	protein_cart_count = 1

	# if there is no current count then set it to 1
	if 'protein_cart_count' not in request.session:
 		request.session['protein_cart_count'] = protein_cart_count
 	else:
 		protein_cart_count = request.session['protein_cart_count']
	
	# del request.session['cart_list']
	# the cart should also be empty
	# when the cart is deleted the reset the count to the number of the deleted cart

	if protein_cart_count == 1:
		for item in cart.items:
			for category in item.product.categories.all():
				if category.title == 'protein':
					print item.product
					cart_2.add(item.product, price=item.product.price)
					cart.remove(item.product)
				else:
					print "no protein inside the cart captain"
		request.session['protein_cart_count'] += 1

	elif protein_cart_count == 2:
		for item in cart.items:
			for category in item.product.categories.all():
				if category.title == 'protein':
					print item.product
					cart_3.add(item.product, price=item.product.price)
					cart.remove(item.product)
				else:
					print "no protein inside the cart captain"
		request.session['protein_cart_count'] += 1
	elif protein_cart_count == 3:
		for item in cart.items:
			for category in item.product.categories.all():
				if category.title == 'protein':
					print item.product
					cart_4.add(item.product, price=item.product.price)
					cart.remove(item.product)
				else:
					print "no protein inside the cart captain"			
		request.session['protein_cart_count'] +=1

	for item in cart_2.items:
		print "cart two items"
		print item


	for item in cart_3.items:
		print "cart three items"
		print item


	for item in cart_4.items:
		print "cart 4 items"
		print item



	return HttpResponse('hmmm')


































