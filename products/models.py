from __future__ import unicode_literals

from django.db import models
from shopping.models import Address

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField()
	categories = models.ManyToManyField('Category')
	benefits = models.ManyToManyField('Benefit')
	serving_size = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=6)

	def __str__(self):
		return self.title + " " + self.serving_size

	def thirty_day(self):
		return round(self.price / 30, 2)


class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=6)

	def __str__(self):
		return self.title


class Research(models.Model):
	product = models.ForeignKey(Product)
	research_title = models.CharField(max_length=120)
	research_article = models.CharField(max_length=120)

	def __str__(self):
		return self.research_title


class Category(models.Model):
	title = models.CharField(max_length=120)

	def __str__(self):
		return self.title

class Benefit(models.Model):
	description = models.CharField(max_length=120)

	def __str__(self):
		return self.description

class Order(models.Model):
	product = models.ManyToManyField(Product)
	transaction_id = models.CharField(max_length=120)
	email = models.EmailField(max_length=120)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	date_ordered = models.DateTimeField()
	total = models.DecimalField(decimal_places=2, max_digits=6)





