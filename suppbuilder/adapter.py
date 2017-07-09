from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from carton.cart import Cart

class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
    	#if the cart has items in it go to checkout
    	cart = Cart(request.session)
    	cart_count = 0

        for product in cart.products:
            cart_count +=1

        if cart_count > 0:
            return  '/shopping/checkout/'
        else:
            return '/suppbuilder/'
