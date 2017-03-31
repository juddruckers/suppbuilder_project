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

	caffeine = Product.objects.get(id=1)
	caffeine_products = Product.objects.all().filter(title='Caffeine')
	caffeine_research = Research.objects.all().filter(product__title='Caffeine')
	caffeine_match = [item for item in caffeine_products if item in cart_items]

	#THEANINE
	theanine = Product.objects.get(id=2)
	theanine_products = Product.objects.all().filter(title='Theanine')
	theanine_research = Research.objects.all().filter(product__title='Theanine')
	theanine_match = [item for item in theanine_products if item in cart_items]

	#CREATINE
	creatine = Product.objects.get(id=22)
	creatine_products = Product.objects.all().filter(title='Creatine')
	creatine_research = Research.objects.all().filter(product__title='Creatine')
	creatine_match = [item for item in creatine_products if item in cart_items]

	# BETA ALANINE
	beta_alanine = Product.objects.get(id=24)
	beta_alanine_products = Product.objects.all().filter(title='Beta Alanine')
	beta_alanine_research = Research.objects.all().filter(product__title='Beta Alanine')
	beta_alanine_match = [item for item in beta_alanine_products if item in cart_items]

	bcaa = Product.objects.get(id=28)
	bcaa_products = Product.objects.all().filter(title='BCAA')
	bcaa_research = Research.objects.all().filter(product__title='BCAA')
	bcaa_match = [item for item in bcaa_products if item in cart_items]

	citrulline_malate = Product.objects.get(id=29)
	citrulline_malate_products = Product.objects.all().filter(title='Citrulline Malate')
	citrulline_malate_research = Research.objects.all().filter(product__title='Citrulline Malate')
	citrulline_malate_match = [item for item in citrulline_malate_products if item in cart_items]

	context = {	
		'caffeine' : caffeine,
		'caffeine_match' : caffeine_match,
		'caffeine_products' : caffeine_products,
		'caffeine_research' : caffeine_research,
		'theanine_match' : theanine_match,
		'theanine' : theanine,
		'theanine_products' : theanine_products,
		'theanine_research' :theanine_research,
		'creatine_match' : creatine_match,
		'creatine' : creatine,
		'creatine_products' : creatine_products,
		'creatine_research' : creatine_research,
		'beta_alanine_match' : beta_alanine_match,
		'beta_alanine' : beta_alanine,
		'beta_alanine_products' : beta_alanine_products,
		'beta_alanine_research' : beta_alanine_research,
		'bcaa_match' : bcaa_match,
		'bcaa' : bcaa,
		'bcaa_products' : bcaa_products,
		'bcaa_research' : bcaa_research,
		'citrulline_malate_match' : citrulline_malate_match,
		'citrulline_malate' : citrulline_malate,
		'citrulline_malate_products' : citrulline_malate_products,
		'citrulline_malate_research' : citrulline_malate_research,
	}

	return render (request, 'products/energy.html', context)



def EnergyTwoView(request):
	locale.setlocale(locale.LC_ALL, "")
	# CART CHECK
	cart = Cart(request.session)
	cart_items = []
	for item in cart.items:
		cart_items.append(item.product)


	# CAFFEINE

	caffeine = Product.objects.get(id=1)
	caffeine_products = Product.objects.all().filter(title='Caffeine')
	caffeine_research = Research.objects.all().filter(product__title='Caffeine')
	caffeine_match = [item for item in caffeine_products if item in cart_items]

	#THEANINE
	theanine = Product.objects.get(id=2)
	theanine_products = Product.objects.all().filter(title='Theanine')
	theanine_research = Research.objects.all().filter(product__title='Theanine')
	theanine_match = [item for item in theanine_products if item in cart_items]

	#CREATINE
	creatine = Product.objects.get(id=22)
	creatine_products = Product.objects.all().filter(title='Creatine')
	creatine_research = Research.objects.all().filter(product__title='Creatine')
	creatine_match = [item for item in creatine_products if item in cart_items]

	# BETA ALANINE
	beta_alanine = Product.objects.get(id=24)
	beta_alanine_products = Product.objects.all().filter(title='Beta Alanine')
	beta_alanine_research = Research.objects.all().filter(product__title='Beta Alanine')
	beta_alanine_match = [item for item in beta_alanine_products if item in cart_items]

	bcaa = Product.objects.get(id=28)
	bcaa_products = Product.objects.all().filter(title='BCAA')
	bcaa_research = Research.objects.all().filter(product__title='BCAA')
	bcaa_match = [item for item in bcaa_products if item in cart_items]

	citrulline_malate = Product.objects.get(id=29)
	citrulline_malate_products = Product.objects.all().filter(title='Citrulline Malate')
	citrulline_malate_research = Research.objects.all().filter(product__title='Citrulline Malate')
	citrulline_malate_match = [item for item in citrulline_malate_products if item in cart_items]

	context = {	
		'caffeine' : caffeine,
		'caffeine_match' : caffeine_match,
		'caffeine_products' : caffeine_products,
		'caffeine_research' : caffeine_research,
		'theanine_match' : theanine_match,
		'theanine' : theanine,
		'theanine_products' : theanine_products,
		'theanine_research' :theanine_research,
		'creatine_match' : creatine_match,
		'creatine' : creatine,
		'creatine_products' : creatine_products,
		'creatine_research' : creatine_research,
		'beta_alanine_match' : beta_alanine_match,
		'beta_alanine' : beta_alanine,
		'beta_alanine_products' : beta_alanine_products,
		'beta_alanine_research' : beta_alanine_research,
		'bcaa_match' : bcaa_match,
		'bcaa' : bcaa,
		'bcaa_products' : bcaa_products,
		'bcaa_research' : bcaa_research,
		'citrulline_malate_match' : citrulline_malate_match,
		'citrulline_malate' : citrulline_malate,
		'citrulline_malate_products' : citrulline_malate_products,
		'citrulline_malate_research' : citrulline_malate_research,
	}

	return render (request, 'products/energytwo.html', context)


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



	whey = Product.objects.get(id=10)
	# print locale.currency(caffeine.price, grouping=True)
	whey_products = Product.objects.all().filter(title='Whey Protein')
	whey_research = Research.objects.all().filter(product__title='Whey Protein')


	print whey.description
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
		'soy_protein_research' : soy_protein_research
	}

	return render (request, 'products/protein.html', context)





































