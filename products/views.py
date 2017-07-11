from django.views.generic import ListView
from .models import Product, Variation , Research
from django.shortcuts import render
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
	# CART CHECK
	cart = Cart(request.session)
	cart_items = []

	flavors = Product.objects.filter(benefits__description__startswith='flavor')
	print flavors
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
	beta_alanine = Product.objects.get(id=25)
	beta_alanine_products = Product.objects.all().filter(title='Beta Alanine')
	beta_alanine_research = Research.objects.all().filter(product__title='Beta Alanine')
	beta_alanine_match = [item for item in beta_alanine_products if item in cart_items]

	
	bcaa = Product.objects.get(id=28)
	bcaa_products = Product.objects.all().filter(title__contains='BCAA')
	bcaa_research = Research.objects.all().filter(product__title='BCAA')
	bcaa_match = [item for item in bcaa_products if item in cart_items]


	citrulline_malate = Product.objects.get(id=31)
	citrulline_malate_products = Product.objects.all().filter(title='Citrulline Malate')
	citrulline_malate_research = Research.objects.all().filter(product__title='Citrulline Malate')
	citrulline_malate_match = [item for item in citrulline_malate_products if item in cart_items]


	glutamine = Product.objects.get(id=71)
	glutamine_products = Product.objects.all().filter(title='Glutamine')
	glutamine_research = Research.objects.all().filter(product__title='Glutamine')
	glutamine_match = [item for item in glutamine_products if item in cart_items]


	acetyl_l_carnitine = Product.objects.get(id=67)
	acetyl_l_carnitine_products = Product.objects.all().filter(title='Acetyl-L Carnitine')
	acetyl_l_carnitine_research = Research.objects.all().filter(product__title='Acetyl-L Carnitine')
	acetyl_l_carnitine_match = [item for item in acetyl_l_carnitine_products if item in cart_items]


	ornithine = Product.objects.get(id=51)
	ornithine_products = Product.objects.all().filter(title='Ornithine HCL')
	ornithine_research = Research.objects.all().filter(product__title='Ornithine HCL')
	ornithine_match = [item for item in ornithine_products if item in cart_items]


	taurine = Product.objects.get(id=57)
	taurine_products = Product.objects.all().filter(title='Taurine')
	taurine_research = Research.objects.all().filter(product__title='Taurine')
	taurine_match = [item for item in taurine_products if item in cart_items]


	ashwagandha = Product.objects.get(id=73)
	ashwagandha_products = Product.objects.all().filter(title='Ashwagandha')
	ashwagandha_research = Research.objects.all().filter(product__title='Ashwagandha')
	ashwagandha_match = [item for item in ashwagandha_products if item in cart_items]


	cordyceps = Product.objects.get(id=75)
	cordyceps_products = Product.objects.all().filter(title='Cordyceps')
	cordyceps_research = Research.objects.all().filter(product__title='Cordyceps')
	cordyceps_match = [item for item in cordyceps_products if item in cart_items]


	rhodiola_rosea = Product.objects.get(id=74)
	rhodiola_rosea_products = Product.objects.all().filter(title='Rhodiola Rosea')
	rhodiola_rosea_research = Research.objects.all().filter(product__title='Rhodiola Rosea')
	rhodiola_rosea_match = [item for item in rhodiola_rosea_products if item in cart_items]


	hmb = Product.objects.get(id=79)
	hmb_products = Product.objects.all().filter(title='HMB')
	hmb_research = Research.objects.all().filter(product__title='HMB')
	hmb_match = [item for item in hmb_products if item in cart_items]


	# alpha_lipoic_acid = Product.objects.get(id=80)
	alpha_lipoic_acid_products = Product.objects.all().filter(title='Alpha Lipoic Acid')
	alpha_lipoic_acid_research = Research.objects.all().filter(product__title='Alpha Lipoic Acid')
	alpha_lipoic_acid_match = [item for item in alpha_lipoic_acid_products if item in cart_items]


	l_tyrosine = Product.objects.get(id=60)
	l_tyrosine_products = Product.objects.all().filter(title='L-Tyrosine')
	l_tyrosine_research = Research.objects.all().filter(product__title='L-Tyrosine')
	l_tyrosine_match = [item for item in l_tyrosine_products if item in cart_items]	

	betaine = Product.objects.get(id=82)
	betaine_products = Product.objects.all().filter(title='Betaine Anhydrous')
	betaine_research = Research.objects.all().filter(product__title='Betaine Anhydrous')
	betaine_match = [item for item in betaine_products if item in cart_items]

	flavor_products = Product.objects.filter(categories__title__startswith='flavor')
	flavor_match = [item for item in flavor_products if item in cart_items]


	context = {	
		'caffeine' : caffeine,
		'caffeine_match' : caffeine_match,
		'caffeine_products' : caffeine_products,
		'caffeine_research' : caffeine_research,
		'glutamine' : glutamine,
		'glutamine_match' : glutamine_match,
		'glutamine_products' : glutamine_products,
		'glutamine_research' : glutamine_research,
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
		'acetyl_l_carnitine_match' : acetyl_l_carnitine_match,
		'acetyl_l_carnitine' : acetyl_l_carnitine,
		'acetyl_l_carnitine_products' : acetyl_l_carnitine_products,
		'acetyl_l_carnitine_research' : acetyl_l_carnitine_research,
		'ornithine_match' : ornithine_match,
		'ornithine' : ornithine,
		'ornithine_products' : ornithine_products,
		'ornithine_research' : ornithine_research,
		'taurine_match' : taurine_match,
		'taurine' : taurine,
		'taurine_products' : taurine_products,
		'taurine_research' : taurine_research,
		'ashwagandha_match' : ashwagandha_match,
		'ashwagandha' : ashwagandha,
		'ashwagandha_products' : ashwagandha_products,
		'ashwagandha_research' : ashwagandha_research,
		'cordyceps_match' : cordyceps_match,
		'cordyceps' : cordyceps,
		'cordyceps_products' : cordyceps_products,
		'cordyceps_research' : cordyceps_research,
		'rhodiola_rosea_match' : rhodiola_rosea_match,
		'rhodiola_rosea' : rhodiola_rosea,
		'rhodiola_rosea_products' : rhodiola_rosea_products,
		'rhodiola_rosea_research' : rhodiola_rosea_research,
		'hmb_match' : hmb_match,
		'hmb' : hmb,
		'hmb_products' : hmb_products,
		'hmb_research' : hmb_research,
		'l_tyrosine_match' : l_tyrosine_match,
		'l_tyrosine' : l_tyrosine,
		'l_tyrosine_products' : l_tyrosine_products,
		'l_tyrosine_research' : l_tyrosine_research,
		'betaine_match' : betaine_match,
		'betaine' : betaine,
		'betaine_products' : betaine_products,
		'betaine_research' : betaine_research,
		'flavor_products' : flavor_products,
		'flavor_match' : flavor_match,
	}

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


































