from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import braintree
from allauth.account.views import *


def IndexView(request):
    
    template_name = 'suppbuilder/index.html'

    current_user = request.user

    print current_user.is_anonymous
    current_user_id = str(request.user.id)


    print "This is the %s" % (current_user)


    # try:
    # 	brain_tree_user = braintree.Customer.find(current_user_id)
    # 	if brain_tree_user == None:
    # 		print "not a customer"
    # 	else:
    # 		print "we have a customer"
    # except:
    # 	pass




    return render(request, 'suppbuilder/index.html')

 
