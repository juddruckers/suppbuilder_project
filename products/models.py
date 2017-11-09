from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from shopping.models import Address
import decimal

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField()
	categories = models.ManyToManyField('Category', blank=True)
	benefits = models.ManyToManyField('Benefit', blank=True)
	
	def __str__(self):
		return self.title

class Variation(models.Model):
	product = models.ForeignKey(Product)
	sku = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=6)
	serving_size = models.CharField(max_length=120)

	def __str__(self):
		return self.product.title + ": " + self.serving_size

	def thirty_day(self):
		"""
		this method returns price per serving for a 30 day supply

		initial = the variations price divided for 30 to
				  symbolize a 30 day supply.
		
		use the quantize method to round the number up
		"""
		initial = decimal.Decimal(self.price / 30, 2)
		cents = decimal.Decimal('.01')
		total = initial.quantize(cents, decimal.ROUND_HALF_UP)
		return total

	def cost(self):
		return "{0:.2f}".format(self.price)


class Benefit(models.Model):
	description = models.CharField(max_length=120)

	def __str__(self):
		return self.description

class Research(models.Model):
	product = models.CharField(max_length=120)
	title = models.CharField(max_length=300)
	article = models.CharField(max_length=300)
	product_effect = models.ManyToManyField(Benefit)

	def __str__(self):
		product_and_study = str(self.product) + ": " + str(self.title)
		return product_and_study


class Category(models.Model):
	title = models.CharField(max_length=120)

	def __str__(self):
		return self.title
  
class Discount(models.Model):
	discount = models.DecimalField(decimal_places=0, max_digits=6)
	email = models.EmailField(max_length=120)
	code = models.CharField(max_length=120)

	def __str__(self):
		return self.code


