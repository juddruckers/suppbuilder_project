from django.views.generic import ListView
from .models import Product
from django.shortcuts import render
# Create your views here.


def EnergyView(request):
	energy = Product.objects.all()

	return render (request, 'products/energy.html', {'energy_list' : energy})