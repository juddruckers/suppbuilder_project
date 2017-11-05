from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods
from django.conf import settings
import decimal
import stripe
import locale
import json
import time
from allauth.account.forms import LoginForm
from carton.cart import Cart
from products.models import Product, Variation , Discount
from .models import Address, Guest, Order
from .forms import AddressForm, EditAddressForm, AuthAddressForm, EditAuthAddressForm, NewAuthAddressForm, EditExistingAddressForm, CreateNewAddressForm
# Create your views here.


def preWorkoutAdd(request):
    """
    this is the view that takes in the variation id and adds it to the cart

    the view receives the the variation ID via ajax. The ID should be
    an integer.

    Find the variation using the variation ID and add it to the cart.
    """
    cart = Cart(request.session)
    variation = Variation.objects.get(id=request.POST.get('variation'))
    cart.add(variation, price=variation.price)

    return HttpResponse("added")

def preWorkoutRemove(request):
    """
    this is the view that takes in the product id and removes it from the cart
    
    the view receives the the variation ID via ajax. The ID should be
    an integer.

    Find the variation using the variation ID and renmove it to the cart.
    """

    # retrieve the cart session object

    cart = Cart(request.session)
    variation = Variation.objects.get(id=request.POST.get('variation'))
    cart.remove(variation)

    return HttpResponse("item removed")

def show(request):
    cart = Cart(request.session)
    # cart.clear()

    grand_total = cart.total 

    per_serving = "{0:.2f}".format(round(grand_total / 30, 2))

    context = {
        'cart' : cart,
        'grand_total' : grand_total,
        'per_serving' : per_serving, 
    }

    return render(request, 'shopping/show-cart.html', context)


def DiscountFindView(request):
    name = request.POST.get('name')
    order_id = request.session['order_id']
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

    order = stripe.Order.retrieve(order_id)
    discount_amount = ''

    for item in order['items']:
        if item['type'] == 'discount':

            return HttpResponse('Discount already applied')

    try:
        coupon = stripe.Coupon.retrieve(name)

        order.coupon = coupon.id

        order.save()

        # create a variable that contains the discounted amount add that to the data returned

        for item in order['items']:
            if item.type == 'discount':
                discount_amount = item.amount
        data = {
        'order' : order,
        'discount_amount' : discount_amount,
        }       
        return HttpResponse(json.dumps(data, indent=2, sort_keys=True))
    except Exception as e:
        coupon = "Invalid code"
        return HttpResponse(coupon)

def CheckoutAddressDeleteView(request):
    """
    This view take the pk of the address that the user wants deleted

    after the address is deleted query for the remaining addresses

    get the first address and make it the default address

    if there is no address list it should go to the auth address view

    so the user can enter an address and continue to checkout
    """
    pk = request.POST.get('pk')
    address = Address.objects.get(id=pk)
    address.delete()    
    user = request.user

    try:
        new_default_address = Address.objects.filter(email=user.email, address_type='shipping').first()
    except:
        new_default_address = None

    print new_default_address

    if new_default_address != None:
        Address.objects.filter(email=user.email, pk=new_default_address.id).update(default_address=True)

    return HttpResponse("address deleted sir")



def AddressChangeView(request):
    current_user = request.user
    current_address = request.POST.get('selected_address')

    print current_address
    address_list = Address.objects.filter(email=current_user.email, address_type='shipping')
    Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)
    Address.objects.filter(id=current_address).update(default_address=True)
    
    return HttpResponse('address changed')

def AddressUpdateView(request, pk):

    current_user = request.user

    if request.method == 'POST':

        address_data = AddressForm(request.POST)

        if address_data.is_valid():

            Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)            

            address, created = Address.objects.update_or_create(
                first_name = address_data.cleaned_data['first_name'],
                last_name = address_data.cleaned_data['last_name'],
                street_address= address_data.cleaned_data['street_address'],
                extended_address= address_data.cleaned_data['extended_address'],
                city= address_data.cleaned_data['city'], 
                state= address_data.cleaned_data['state'],
                zip_code= address_data.cleaned_data['zip_code'],
                email= address_data.cleaned_data['email'],
                address_type= address_data.cleaned_data['address_type'],                
            )

            address_list = Address.objects.filter(email=current_user.email, address_type='shipping')

            return render (request, 'shopping/shipping.html', {'address_list': address_list,})           

    else:

        address = Address.objects.get(id=pk)

        Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)
        Address.objects.filter(id=pk).update(default_address=True)

        existing_address_form = EditAddressForm(initial={
                'first_name' : address.first_name,
                'last_name' : address.last_name,
                'street_address' : address.street_address,
                'extended_address' : address.extended_address,
                'city' : address.city, 
                'state' : address.state,
                'zip_code' : address.zip_code,
                'email' : address.email,
            })

        pk = Address.objects.get(id=pk)

        return render(request, 'shopping/address_form.html', {'form': existing_address_form, 'address': address, 'pk':pk})

def CheckOutAddressUpdateView(request, pk):

    """
    This is the address view that the user will come across from the checkout page
    on edit or delete of address it will return to the 
    selected shipping address 
    """

    current_user = request.user

    if request.method == 'POST':

        address_data = AddressForm(request.POST)

        if address_data.is_valid():

            Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)            

            address, created = Address.objects.update_or_create(
                first_name = address_data.cleaned_data['first_name'],
                last_name = address_data.cleaned_data['last_name'],
                street_address= address_data.cleaned_data['street_address'],
                extended_address= address_data.cleaned_data['extended_address'],
                city= address_data.cleaned_data['city'], 
                state= address_data.cleaned_data['state'],
                zip_code= address_data.cleaned_data['zip_code'],
                email= address_data.cleaned_data['email'],
                address_type= address_data.cleaned_data['address_type'],

            )

            if address:
                Address.objects.filter(email=current_user.email, address_type='shipping', pk=pk).update(default_address=True) 

            address_list = Address.objects.filter(email=current_user.email, address_type='shipping')

            return render (request, 'shopping/select-shipping-address.html', {'address_list': address_list,})           

    else:

        address = Address.objects.get(id=pk)

        Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)
        Address.objects.filter(id=pk).update(default_address=True)

        existing_address_form = EditAddressForm(initial={
                'first_name' : address.first_name,
                'last_name' : address.last_name,
                'street_address' : address.street_address,
                'extended_address' : address.extended_address,
                'city' : address.city, 
                'state' : address.state,
                'zip_code' : address.zip_code,
                'email' : address.email,
            })

        pk = Address.objects.get(id=pk)

        return render(request, 'shopping/address_form.html', {'form': existing_address_form, 'address': address, 'pk':pk})

def payment_view(request):
    user = request.user

    cart = Cart(request.session)
    cart_count = 0
    cart_total = cart.total
    item_list =[]
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

    if user.is_anonymous():
        
        form = LoginForm()
        return render(request, 'account/login.html', {'form' : form})

    if user.is_authenticated():

        shipping_address = Address.objects.filter(email=request.user.email, address_type='shipping', default_address=True).first()

        if not shipping_address:
            form = AuthAddressForm(initial={
                'address_type' : 'shipping',
                'email' : user.email,
            })
            return render(request, 'shopping/address.html', {'form': form,})
        
        else:

            for product in cart.products:
                b = {
                "type" : 'sku',
                "parent" : product.sku,
                "quantity" : 1,
                }
                item_list.append(b)

            if 'order_id' in request.session:
                
                order = stripe.Order.retrieve(request.session['order_id'])
                order_items = [item for item in order['items'] if item.type == 'sku']

                if len(item_list) != len(order_items):
                    order.metadata['cancelation'] = "Order has been canceled due to updated cart"
                    order.save()
                    order = stripe.Order.create(
                      currency = 'usd',
                      email = user.email,
                      items = item_list,
                      shipping = {
                        "name": user.first_name + " " + user.last_name,
                        "address":{
                          "line1": shipping_address.street_address,
                          "city": shipping_address.city,
                          "country":'US',
                          "postal_code": shipping_address.zip_code,
                          "state" : shipping_address.state,
                        }
                      },
                    )
                    print "items have changed creating new order"

                    request.session['order_id'] = order.id

            else:
                
                order = stripe.Order.create(
                  currency = 'usd',
                  email = user.email,
                  items = item_list,
                  shipping = {
                    "name": user.first_name + " " + user.last_name,
                    "address":{
                      "line1": shipping_address.street_address,
                      "city": shipping_address.city,
                      "country":'US',
                      "postal_code": shipping_address.zip_code,
                      "state" : shipping_address.state,
                    }
                  },
                )

                request.session['order_id'] = order.id

            discount = False
            discount_amount = 0
            default_shipping_amount = ''
            tax_amount = ''        
            shipping_options = []
            order_amount = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

            for item in order['items']:
                if item['type'] == 'shipping':
                    default_shipping_amount = decimal.Decimal(item['amount']) / 100
                elif item['type'] == 'tax':
                    tax_amount = decimal.Decimal(item['amount']) / 100
                elif item['type'] == 'discount':
                    discount = True
                    discount_amount = "%0.2f" % (decimal.Decimal(item.amount) / 100)
            
            for shipping_method in order.shipping_methods:
                b = {
                    "description" : shipping_method.description,
                    "amount" : "%0.2f" % (decimal.Decimal(shipping_method.amount) / 100),
                    'id' : shipping_method.id,
                    'delivery_estimate' : shipping_method.delivery_estimate.date,
                }
                
                shipping_options.append(b)

            context ={
                'shipping_address': shipping_address,
                'cart_count' : cart_count,
                'cart_total' : cart_total,
                'order' : order,
                'order_amount' : order_amount,
                'shipping_options' : shipping_options,
                'default_shipping_amount' : default_shipping_amount,
                'tax_amount' : tax_amount,
                'user' : user,
                'discount' : discount,
                'discount_amount' : discount_amount
            }

            return render(request, 'shopping/stripe-payment.html', context)

def StripeAddressView(request):
    """
    This is the view the user will go to when they go to checkout and they have no
    address on file for them. Once they create an address it will create an order and 
    redirect them to the payment view.

    This will also be the page where they will be directed to if they want to
    change the address from the payment view. It will create or update a shipping
    address and update the old order to a canceled state due to address change.
    It will then create a new order and redirect to the payment view
    """

    user = request.user

    if request.method == 'POST':

        address_data = AddressForm(request.POST)

        if address_data.is_valid():

            """
            if the address data is valid change all existing shipping addresses
            default_address attribute to False.
            """
            Address.objects.filter(email=user.email, address_type='shipping').update(default_address=False)            

            address, created = Address.objects.update_or_create(
                first_name = address_data.cleaned_data['first_name'].lower(),
                last_name = address_data.cleaned_data['last_name'],
                street_address= address_data.cleaned_data['street_address'].lower(),
                extended_address= address_data.cleaned_data['extended_address'].lower(),
                city= address_data.cleaned_data['city'].lower() , 
                state= address_data.cleaned_data['state'],
                zip_code= address_data.cleaned_data['zip_code'],
                email= address_data.cleaned_data['email'],
                address_type= address_data.cleaned_data['address_type'],                
            )

            cart = Cart(request.session)
            cart_count = 0
            cart_total = cart.total
            item_list =[]

            for product in cart.products:
                b = {
                "type" : 'sku',
                "parent" : product.sku,
                "quantity" : 1,
                }

                item_list.append(b)

            for product in cart.products:
                cart_count +=1

            stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
            
            if 'order_id' in request.session:
                order = stripe.Order.retrieve(request.session['order_id'])
                order.metadata['cancelation'] = "Order has been canceled due to new shipping address"
                order.save()
                
                order = stripe.Order.create(
                  currency = 'usd',
                  email = user.email,
                  items = item_list,
                  shipping = {
                    "name": user.first_name + " " + user.last_name,
                    "address":{
                      "line1": address.street_address,
                      "city": address.city,
                      "country":'US',
                      "postal_code": address.zip_code,
                      "state" : address.state,
                    }
                  },
                )

                request.session['order_id'] = order.id
                
                return redirect('checkout-view')

            else:
                order = stripe.Order.create(
                  currency = 'usd',
                  email = user.email,
                  items = item_list,
                  shipping = {
                    "name": user.first_name + " " + user.last_name,
                    "address":{
                      "line1": address.street_address,
                      "city": address.city,
                      "country":'US',
                      "postal_code": address.zip_code,
                      "state" : address.state,
                    }
                  },
                )

                request.session['order_id'] = order.id

                return redirect('checkout-view')

            # default_shipping_amount = ''
            # tax_amount = ''        
            # shipping_options = []
            # order_amount = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

            # for item in order['items']:
            #     if item['type'] == 'shipping':
            #         default_shipping_amount = decimal.Decimal(item['amount']) / 100
            #     elif item['type'] == 'tax':
            #         tax_amount = decimal.Decimal(item['amount']) / 100
            
            
            # for shipping_method in order.shipping_methods:
            #     b = {
            #         "description" : shipping_method.description,
            #         "amount" : decimal.Decimal(shipping_method.amount) / 100,
            #         'id' : shipping_method.id,
            #         'delivery_estimate' : shipping_method.delivery_estimate.date,
            #     }
                
            #     shipping_options.append(b)


            # context ={
            #     'shipping_address': address,
            #     'cart_count' : cart_count,
            #     'cart_total' : cart_total,
            #     'order' : order,
            #     'order_amount' : order_amount,
            #     'shipping_options' : shipping_options,
            #     'default_shipping_amount' : default_shipping_amount,
            #     'tax_amount' : tax_amount,
            # }

            # return render(request, 'shopping/stripe-payment.html', context)

        else:
            print "data is not clean"
            errors =  address_data.errors

            form = AuthAddressForm(initial={
                'first_name' : request.user.first_name,
                'last_name' : request.user.last_name,
                'email' : request.user.email,
            })
            return render(request, 'shopping/address.html', {'form': form, 'errors': errors}) 

    else:
        print 'no post data receieved EditAuthUserAddressView'
            
        form = AuthAddressForm(initial={
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
        })

        return render(request, 'shopping/address.html', {'form': form,})

def StripePaymentView(request):

    """
    This is the view that will process the payment and send the user to the 
    order detail page.

    The token will be recieved from the stripe payment form

    the order_id will be taken from the session variable set whenever a new order is created

    using the order_id retrieve the stripe order_id

    using the token pay the retrieved order_id

    clear the cart once the order is finished 

    """
    user = request.user 
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    cart = Cart(request.session)
    token = request.POST.get('stripeToken')
    order_id = request.session['order_id']
    order = stripe.Order.retrieve(order_id)
    order.pay(source = token)
    saved_order = Order(email = user.email, order_id = order.id)
    saved_order.save()

    item_count = 0
    tax_amount = 0
    shipping_amount = ''
    item_amount = 0
    discount_amount = 0


    total = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

    for item in order['items']:
        if item['type'] == 'sku':
            item_count += 1
            item_amount += decimal.Decimal(item['amount'])
        elif item['type'] == 'tax':
            tax_amount = "{0:.2f}".format(decimal.Decimal(item['amount']) / 100)
        elif item['type'] == 'shipping':
            shipping_amount = "{0:.2f}".format(decimal.Decimal(item['amount']) / 100)
        elif item['type'] == 'discount':
            discount_amount = "{0:.2f}".format(decimal.Decimal(item['amount']) / 100)


    item_total = "{0:.2f}".format(decimal.Decimal(item_amount) / 100)

    context = {
    'order' : order,
    'item_count' : item_count,
    'total' : total,
    'tax_amount' : tax_amount,
    'shipping_amount' : shipping_amount,
    'item_total' : item_total,
    'discount_amount': discount_amount,
    }


    cart.clear()
    del request.session['order_id']

    return render(request, 'shopping/order-summary.html', context)


def AddressView(request):

    form = AddressForm()
    current_user = request.user
    customer_id = str(current_user.id)

    print 'no post data receieved'

    form = AuthAddressForm(initial={
        'first_name' : current_user.first_name,
        'last_name' : current_user.last_name,
        'email' : current_user.email,
        })
        
    return render(request, 'shopping/address.html', {'form': form,})    


@login_required(login_url='/accounts/login/')
@require_http_methods(["GET", "POST"])
def ShippingView(request):

    """
    this is the profile shipping view
    this will display all of the users shipping addresses

    on post it will validate the data and return them to the list of shipping options
    """

    current_user_email = request.user.email

    current_user = request.user

    address_list = Address.objects.filter(email=current_user_email, address_type='shipping')



    if address_list:
        print address_list
        return render(request, 'shopping/shipping.html', {'address_list': address_list, 'current_user': current_user})
    else:
        print "there is no address_list"
        return render(request, 'shopping/address.html', {'form': AuthAddressForm})  

@login_required(login_url='/accounts/login/')
def SelectShippingView(request):
    """
    this is the page where the user will find all of their address to select 

    on select they will go back to the checkout page with
    """

    current_user_email = request.user.email

    current_user = request.user

    address_list = Address.objects.filter(email=current_user_email, address_type='shipping')

    if address_list:
        print address_list
        return render(request, 'shopping/select-shipping-address.html', {'address_list': address_list, 'current_user': current_user})
    else:
        print "there is no address_list"
        return render(request, 'shopping/address.html', {'form': AuthAddressForm}) 

@login_required(login_url='/accounts/login/')
def OrdersView(request):
    """
    This is the view that will display all of the current logged in users past orders
    """
    user = request.user

    try:
     os.environ['SECRETKEY']
    except:
        print "no environment variable"
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

    order_query = Order.objects.filter(email=user.email)

    orders = [str(order.order_id) for order in order_query]

    stripe_orders = stripe.Order.list(ids=orders)

    print stripe_orders
    order_details = []

    for order in stripe_orders:
        b = {}
        i = []
        b['order_id'] = str(order.id)
        a = decimal.Decimal(order.amount) / 100
        b['amount'] = a
        t = time.strftime('%Y-%m-%d', time.localtime(order.created))
        b['order_created'] = t
        s = order.shipping
        b['shipping'] = s
        for item in order['items']:
            if item.type == 'sku':
                i.append(item.description)
        b['items'] = i
        os = (order.status).title()
        b['order_status'] = os
        order_details.append(b)


    # for order in stripe_orders:
    #     b = {}
    #     b['amount'] = decimal.Decimal(order.amount)/100
    #     for item in order['items']:
    #         if item['type'] == 'shipping':
    #             a = decimal.Decimal(item['amount'])/100
    #             b['shipping'] = a
    #         elif item['type'] == 'tax':
    #             t = decimal.Decimal(item['tax'])/100
    #             b['tax'] = t
    #     order_details.append(b)
    return render(request, 'shopping/past-orders.html', {"order_details": order_details,})

@login_required(login_url='/accounts/login/')
def OrderDetailView(request, order_id):
    """
    this is the view that will take the id of the stripe order and take the to an order detail page
    """

    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    
    order = stripe.Order.retrieve(order_id)

    return render(request, 'shopping/order-detail.html', {'order' : order})

@login_required(login_url='/accounts/login/')
def ProfileView(request):
    current_user = request.user



    shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping')


    print "printing address count below"

    context = {
        'current_user' : current_user,
        'shipping_address' : shipping_address,
    }

    return render(request, 'shopping/profile.html', context)

def StripePaymentView(request):

    """
    This is the view that will process the payment and send the user to the 
    order detail page.

    The token will be recieved from the stripe payment form

    the order_id will be taken from the session variable set whenever a new order is created

    using the order_id retrieve the stripe order_id

    using the token pay the retrieved order_id

    clear the cart once the order is finished 

    """
    user = request.user 
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    cart = Cart(request.session)
    token = request.POST.get('stripeToken')
    order_id = request.session['order_id']
    # order = stripe.Order.retrieve('or_1AbxbZBjE7taidLcnf5g262l')
    order = stripe.Order.retrieve(order_id)
    order.pay(source = token)
    saved_order = Order(email = user.email, order_id = order.id)
    saved_order.save()

    item_count = 0
    tax_amount = 0
    shipping_amount = ''
    item_amount = 0
    discount_amount = 0


    total = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

    for item in order['items']:
        if item['type'] == 'sku':
            item_count += 1
            item_amount += decimal.Decimal(item['amount'])
        elif item['type'] == 'tax':
            tax_amount = "{0:.2f}".format(decimal.Decimal(item['amount']) / 100)
        elif item['type'] == 'shipping':
            shipping_amount = "{0:.2f}".format(decimal.Decimal(item['amount']) / 100)
        elif item['type'] == 'discount':
            discount_amount = "{0:.2f}".format(decimal.Decimal(item['amount']) / 100)


    item_total = "{0:.2f}".format(decimal.Decimal(item_amount) / 100)

    context = {
    'order' : order,
    'item_count' : item_count,
    'total' : total,
    'tax_amount' : tax_amount,
    'shipping_amount' : shipping_amount,
    'item_total' : item_total,
    'discount_amount': discount_amount,
    }


    cart.clear()
    del request.session['order_id']

    return render(request, 'shopping/order-summary.html', context)

def StripeGuestAddressView(request):
    form = AddressForm()
    current_user = request.user

    # user should always be anonymous here
    if request.user.is_anonymous:
        guest_email = request.session.get('email')
        if guest_email is None:
            form = LoginForm()
            return render(request, 'account/login.html', {'form' : form})

        current_user = Guest.objects.filter(email=guest_email).first()
        customer_id = str(current_user.id)


    if request.method == 'POST':
          
        #create a form instance from POST data
        address_data = AddressForm(request.POST)
        user = request.user

        if address_data.is_valid():


            request.session['guest_first_name'] = address_data.cleaned_data['first_name']
            request.session['guest_last_name'] = address_data.cleaned_data['last_name']
            request.session['guest_street_address'] = address_data.cleaned_data['street_address']
            request.session['guest_extended_address'] = address_data.cleaned_data['extended_address']
            request.session['city'] = address_data.cleaned_data['city']
            request.session['state'] = address_data.cleaned_data['state']
            request.session['zip_code'] = address_data.cleaned_data['zip_code']

            guest_first_name = request.session['guest_first_name'].upper()
            guest_last_name = request.session['guest_last_name'].upper()
            guest_street_address = request.session['guest_street_address'].upper()
            guest_extended_address = request.session['guest_extended_address'].upper()
            guest_city = request.session['city'].upper()
            guest_state = request.session['state'].upper()
            guest_zip = request.session['zip_code']
            guest_email = request.session['email']

            cart = Cart(request.session)
            cart_count = 0
            cart_total = cart.total
            item_list =[]

            for product in cart.products:
                b = {
                "type" : 'sku',
                "parent" : product.sku,
                "quantity" : 1,
                }

                item_list.append(b)

            for product in cart.products:
                cart_count +=1

            stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
            
            if 'order_id' in request.session:
                order = stripe.Order.retrieve(request.session['order_id'])
            else:
                order = stripe.Order.create(
                  currency = 'usd',
                  email = guest_email,
                  items = item_list,
                  shipping = {
                    "name": address_data.cleaned_data['first_name'] + " " + address_data.cleaned_data['last_name'],
                    "address":{
                      "line1": address_data.cleaned_data['street_address'],
                      "city": address_data.cleaned_data['city'],
                      "country":'US',
                      "postal_code": address_data.cleaned_data['zip_code'],
                      "state" : address_data.cleaned_data['state'],
                    }
                  },
                )

                request.session['order_id'] = order.id

            default_shipping_amount = ''
            tax_amount = ''        
            shipping_options = []
            order_amount = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

            for item in order['items']:
                if item['type'] == 'shipping':
                    default_shipping_amount = decimal.Decimal(item['amount']) / 100
                elif item['type'] == 'tax':
                    tax_amount = decimal.Decimal(item['amount']) / 100
            
            
            for shipping_method in order.shipping_methods:
                b = {
                    "description" : shipping_method.description,
                    "amount" : decimal.Decimal(shipping_method.amount) / 100,
                    'id' : shipping_method.id,
                    'delivery_estimate' : shipping_method.delivery_estimate.date,
                }
                
                shipping_options.append(b)

            context = {
                'cart_count' : cart_count,
                'cart_total' : cart_total,
                'order' : order,
                'order_amount' : order_amount,
                'shipping_options' : shipping_options,
                'default_shipping_amount' : default_shipping_amount,
                'tax_amount' : tax_amount,
                'guest_first_name' : guest_first_name,
                'guest_last_name' : guest_last_name,
                'guest_street_address' : guest_street_address,
                'guest_extended_address' : guest_extended_address,
                'guest_city' : guest_city,
                'guest_state' :guest_state,
                'guest_zip' : guest_zip,
                'guest_email' : guest_email,
                'user' : user,
            }


            return render(request, 'shopping/stripe-payment.html', context)

        else:
            print "data is not clean"
            errors =  address_data.errors
            return render(request, 'shopping/address.html', {'form': AddressForm, 'errors': errors}) 

    else:
        print 'no post data receieved'
            
        return render(request, 'shopping/address.html', {'form': AddressForm,})

def NewAddressView(request):

    """
    This is the address form creation page when they are going from the checkout page

    if they click add new addresss they will get this page

    from here create a new order since there is a new address and go straight to the checkout page
    """

    user = request.user
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    cart = Cart(request.session)
    cart_count = 0
    cart_total = cart.total
    item_list =[]

    if request.method == 'POST':

        address_data = NewAuthAddressForm(request.POST)

        if address_data.is_valid():

            Address.objects.filter(email=user.email, address_type='shipping').update(default_address=False) 

            address, created = Address.objects.update_or_create(
                first_name = address_data.cleaned_data['first_name'],
                last_name = address_data.cleaned_data['last_name'],
                street_address= address_data.cleaned_data['street_address'],
                extended_address= address_data.cleaned_data['extended_address'],
                city= address_data.cleaned_data['city'], 
                state= address_data.cleaned_data['state'],
                zip_code= address_data.cleaned_data['zip_code'],
                email= address_data.cleaned_data['email'],
                address_type= address_data.cleaned_data['address_type'],
                default_address= address_data.cleaned_data['default_address']                 
            )
            
            for product in cart.products:
                b = {
                "type" : 'sku',
                "parent" : product.sku,
                "quantity" : 1,
                }
                item_list.append(b)
                cart_count += 1

            order = stripe.Order.create(
              currency = 'usd',
              email = user.email,
              items = item_list,
              shipping = {
                "name": address.first_name + " " + address.last_name,
                "address":{
                  "line1": address.street_address,
                  "city": address.city,
                  "country":'US',
                  "postal_code": address.zip_code,
                  "state" : address.state,
                }
              },
            )

            request.session['order_id'] = order.id

            discount = False
            discount_amount = 0

            default_shipping_amount = ''
            tax_amount = ''        
            shipping_options = []
            order_amount = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

            for item in order['items']:
                if item['type'] == 'shipping':
                    default_shipping_amount = decimal.Decimal(item['amount']) / 100
                elif item['type'] == 'tax':
                    tax_amount = decimal.Decimal(item['amount']) / 100
                elif item['type'] == 'discount':
                    discount = True
                    discount_amount = "%0.2f" % (decimal.Decimal(item.amount) / 100)
            
            for shipping_method in order.shipping_methods:
                b = {
                    "description" : shipping_method.description,
                    "amount" : "%0.2f" % (decimal.Decimal(shipping_method.amount) / 100),
                    'id' : shipping_method.id,
                    'delivery_estimate' : shipping_method.delivery_estimate.date,
                }
                
                shipping_options.append(b)

            context ={
                'shipping_address': address,
                'cart_count' : cart_count,
                'cart_total' : cart_total,
                'order' : order,
                'order_amount' : order_amount,
                'shipping_options' : shipping_options,
                'default_shipping_amount' : default_shipping_amount,
                'tax_amount' : tax_amount,
                'user' : user,
                'discount' : discount,
                'discount_amount' : discount_amount
            }

            return render(request, 'shopping/stripe-payment.html', context)

    else:

        form = NewAuthAddressForm(initial={
                'email' : request.user.email,
            })

        return render(request, 'shopping/address.html', {'form': form})




def StripeUpdateOrderView(request):

    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
   
    order_id = request.POST.get('order_id')

    order = stripe.Order.retrieve(order_id)
    
    shipping_method = request.POST.get('shipping_method_id')

    order.selected_shipping_method = shipping_method

    order.save()

    shipping_price = [item.amount for item in order['items'] if item.type == 'shipping']

    print shipping_price

    print order['shipping'].address['line1']

    data = {
        'order': order,
        'shipping_price' : shipping_price,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def EditGuestAddressView(request):

    """
    this is the view that takes the guest session variables and populates them into a form 
    for the guest to edit.
    """

    guest_first_name = request.session['guest_first_name'].upper()
    guest_last_name = request.session['guest_last_name'].upper()
    guest_street_address = request.session['guest_street_address'].upper()
    guest_extended_address = request.session['guest_extended_address'].upper()
    guest_city = request.session['city'].upper()
    guest_state = request.session['state'].upper()
    guest_zip = request.session['zip_code']
    guest_email = request.session['email']


    form = AddressForm(initial={
        'first_name': guest_first_name,
        'last_name' : guest_last_name,
        'street_address' : guest_street_address,
        'extended_address' : guest_extended_address,
        'city' : guest_city,
        'state': guest_state,
        'zip_code': guest_zip,
    });

    return render(request, 'shopping/edit-guest-address.html', {'form': form})

@login_required(login_url='/accounts/login/')
def EditAuthCheckoutAddressView(request):

    """
    This is the view that takes the authenticated user to their addresses on file 

    if the request is a post method it will validate the address data
    and then create a new order using the new addresss
    if there is an old order it will delete that old order and state in the meta data why
    after the new address is saved and new order created they are redirected to the checkout page.
    """
    user = request.user

    if request.method == 'POST':
        stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

        address_data = EditAuthAddressForm(request.POST)

        if address_data.is_valid():

            Address.objects.filter(email=user.email, address_type='shipping').update(default_address=False)

            shipping_address, created = Address.objects.update_or_create(
                first_name = address_data.cleaned_data['first_name'],
                last_name = address_data.cleaned_data['last_name'],
                street_address= address_data.cleaned_data['street_address'],
                extended_address= address_data.cleaned_data['extended_address'],
                city= address_data.cleaned_data['city'], 
                state= address_data.cleaned_data['state'],
                zip_code= address_data.cleaned_data['zip_code'],
                email= address_data.cleaned_data['email'],
                address_type= address_data.cleaned_data['address_type'],                
            )

            cart = Cart(request.session)
            cart_count = 0
            cart_total = cart.total
            item_list =[]

            for product in cart.products:
                b = {
                "type" : 'sku',
                "parent" : product.sku,
                "quantity" : 1,
                }

                cart_count +=1

                item_list.append(b)

            old_order = stripe.Order.retrieve(request.session['order_id'])
            old_order.status = 'canceled'
            old_order.metadata['cancelation'] = "Order canceled due to address change"
            old_order.save()

            order = stripe.Order.create(
              currency = 'usd',
              email = user.email,
              items = item_list,
              shipping = {
                "name": shipping_address.first_name + " " + shipping_address.last_name,
                "address":{
                  "line1": shipping_address.street_address,
                  "city": shipping_address.city,
                  "country":'US',
                  "postal_code": shipping_address.zip_code,
                  "state" : shipping_address.state,
                }
              },
            )
            
            request.session['order_id'] = order.id

            default_shipping_amount = ''
            tax_amount = ''        
            shipping_options = []
            order_amount = "{0:.2f}".format(decimal.Decimal(order.amount) / 100)

            for item in order['items']:
                if item['type'] == 'shipping':
                    default_shipping_amount = decimal.Decimal(item['amount']) / 100
                elif item['type'] == 'tax':
                    tax_amount = decimal.Decimal(item['amount']) / 100
            
            
            for shipping_method in order.shipping_methods:
                b = {
                    "description" : shipping_method.description,
                    "amount" : decimal.Decimal(shipping_method.amount) / 100,
                    'id' : shipping_method.id,
                    'delivery_estimate' : shipping_method.delivery_estimate.date,
                }
                
                shipping_options.append(b)        

            context ={
                'shipping_address': shipping_address,
                'cart_count' : cart_count,
                'cart_total' : cart_total,
                'order' : order,
                'order_amount' : order_amount,
                'shipping_options' : shipping_options,
                'default_shipping_amount' : default_shipping_amount,
                'tax_amount' : tax_amount,
                'shipping_address' : shipping_address,
            }

            return render(request, 'shopping/stripe-payment.html', context)

    else:

        print "no post data received"

        address_list = Address.objects.filter(email=user.email, address_type='shipping')

        if len(address_list) == 0:
            form = AuthAddressForm(initial={
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'address_type' : 'shipping',
                'email' : user.email,
            })
            return render(request, 'shopping/address.html', {'form': form,})

        return render (request, 'shopping/select-shipping-address.html', {'address_list': address_list,})



def EditExistingAddressView(request, pk):

    """
    this is the page that will take the existing address ID that is being updated
    with the ID it  will filter the the selection using the current users email address and
    update the object with the new values from the form 

    if the request is a get method it will take the pk given from the request
    and find that address using the pk. It will make all other addresses associated to the user 
    default address to false and make the address being edited the default.

    It will then create an address instance with the pk


    if the request is a post method it takes the pk provided with the form
    finds the address being updated and uses it as the instance in form 
    if the form is valid it updates the address 
    after the address is updated it makes the updated address the default shipping address


    """

    current_user = request.user

    if request.method == 'POST':
        instance = get_object_or_404(Address, id=pk)
        form = EditExistingAddressForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            Address.objects.filter(id=pk).update(default_address=True)
            address_list = Address.objects.filter(email=current_user.email, address_type='shipping')

            return redirect('shipping')          

    else:

        address = Address.objects.get(id=pk)

        Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)
        Address.objects.filter(id=pk).update(default_address=True)

        existing_address_form = EditExistingAddressForm(initial={
                'first_name' : address.first_name,
                'last_name' : address.last_name,
                'street_address' : address.street_address,
                'extended_address' : address.extended_address,
                'city' : address.city, 
                'state' : address.state,
                'zip_code' : address.zip_code,
                'email' : address.email,
            }, pk = pk)

        return render(request, 'shopping/address_form.html', {'form': existing_address_form, })

@login_required(login_url='/accounts/login/')
def AddNewAddressView(request):
    """
    this is the view that that the user will visit with a new form so they can add a new shipping address

    on post they will create a new address and be redirected to their shipping list page from their profile
    """

    user = request.user
    if request.method == 'POST':
        form = CreateNewAddressForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('shipping')

    else:

        form = CreateNewAddressForm(initial={
            'email' : user.email,
            })

        return render(request, 'shopping/address.html', {'form' : form})

































