from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

# Create your models here.


class Address(models.Model):
	address_choices = (
		('billing', 'Billing'),
		('shipping', 'Shipping'),
	)

	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	street_address = models.CharField(max_length=120)
	extended_address = models.CharField(max_length=120, blank=True)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=9)
	address_type = models.CharField(max_length=20, choices=address_choices, default='shipping')
	email = models.CharField(max_length=120, blank=True)
	same = models.BooleanField(default= False)
	default_address = models.BooleanField(default=True)
	brain_tree_code = models.CharField(max_length=2, blank=True)


	def __str__(self):
		return 	self.street_address

	def get_absolute_url(self):
		return reverse('update', kwargs={'pk': self.pk})



class Guest(models.Model):
	email = models.CharField(max_length=120, unique=True)

	def __str__(self):
		return self.email
