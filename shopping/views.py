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
from .forms import AddressForm, AuthAddressForm
# Create your views here.

 
def add_item(request):
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

def remove_item(request):
    """
    this is the view that takes in the product id and removes it from the cart
    
    the view receives the the variation ID via ajax. The ID should be
    an integer.

    Find the variation using the variation ID and renmove it to the cart.
    """

    # retrieve the cart session object
    cart = Cart(request.session)
    variation = Variation.objects.get(id=request.POST.get('variation'))
    print (request.POST.get("variation"))
    print variation
    cart.remove(variation)

    return HttpResponse("item removed")

def cart(request):
    """
    this page will show the cart and all the products inside of the cart

    it will also take a post method to remove all items from the cart 
    that have corresponding ID's in the array.
    """
    cart = Cart(request.session)

    if request.method == "POST":
        # retrieve the list from the ajax request using getlist
        delete_list = (request.POST.getlist("delete_item_list[]"))

        # retrieve all variations using the ID's in the delete_list
        items = Variation.objects.filter(id__in=delete_list)

        # remove the items
        for variation in items:
            cart.remove(variation)

        return HttpResponse("success")

    else:        

        grand_total = cart.total

        # divide the total by 30 to get a price of serving size. The value is still a decimal type
        price_per = (cart.total/30)

        """
        use quantize and round half up to account for times where the price lands at a half

        example: 2.005 => 2.01, 2.015 => 2.02

        if there is no items in the cart trying to quantize 0 will throw an error
        """
        if price_per != 0:
            serving = price_per.quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_HALF_UP)
        else:
            serving = None

        context = {
            'cart' : cart,
            'grand_total' : grand_total,
            'per_serving' : serving, 
        }

        return render(request, 'shopping/show-cart.html', context)

def payment(request):

    """
    View creates a stripe order for the user and directs them to the order confirmation page where
    they can finalize their order and input their payment information using stripe.

    args:
        user: current user
        cart: cart session object that contains all items to be placed in the order
        cart_count: count of items in the cart
        cart_total: total amount of the items in the cart
        shipping_address: address associated to user that is the current default shipping address
        shipping_info: object containing shipping information used to create stripe order.
        item_list: list of item objects used to create stripe order.
        order = stripe order object.

    """
    user = request.user
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    cart = Cart(request.session)
    cart_count = len(cart.items)
    cart_total = cart.total

    if cart_count == 0 and not 'order_id' in request.session:
        return redirect('/')

    # if the user is not logged in or a guest send them to login page
    if user.is_anonymous():        
        form = LoginForm()
        return render(request, 'account/login.html', {'form' : form})

    # if user is logged in
    if user.is_authenticated():

        # find the users addresses and retrieve the default address to be used
        shipping_address = Address.objects.filter(email=request.user.email, address_type='shipping', default_address=True).first()

        # if there is no shipping address redirect them to create an address.
        if not shipping_address:
            # create shipping default value of address type is shipping
            # fill in the email with the current logged in users email
            form = AuthAddressForm(initial={
                'address_type' : 'shipping',
                'email' : user.email,
            })
            return render(request, 'shopping/address.html', {'form': form,})
        
        else:

            shipping_info = {
                        "name": user.first_name + " " + user.last_name,
                        "address":{
                          "line1": shipping_address.street_address,
                          "city": shipping_address.city,
                          "country":'US',
                          "postal_code": shipping_address.zip_code,
                          "state" : shipping_address.state,
                        }
                      }

            # create a list of objects from the items in the cart.
            item_list = [{"type" : 'sku', "parent" : item.sku, "quantity" : 1,} for item in cart.products]

            # look for an order_id in the session
            if 'order_id' in request.session:
                
                # if the order_id exists retrieve the order using the ID
                order = stripe.Order.retrieve(request.session['order_id'])

                """
                if the length of the item list does not match the length of the len of order items
                the order has been changed.

                Stripe does not give the ability to edit the items in an already existing order. 
                cancel old order and create new order
                """
                if len(item_list) != len(order['items']):
                    order.metadata['cancelation'] = "Order has been canceled due to updated cart"
                    order.save()
                    order = stripe.Order.create(
                      currency = 'usd',
                      email = user.email,
                      items = item_list,
                      shipping = shipping_info
                    )
                    request.session['order_id'] = order.id

            # if no order_id in session
            else:
                
                # create order
                order = stripe.Order.create(
                  currency = 'usd',
                  email = user.email,
                  items = item_list,
                  shipping = shipping_info,
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

            context = {
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

def create_address(request):
    """
    This is the view the user will go to when they go to checkout and they have no
    address on file for them. On successful creation they will be redirected to the payment
    page.
    """
    user = request.user

    if request.method == 'POST':

        address_data = AuthAddressForm(request.POST)

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

            return redirect('payment')

        else:
            print "data is not clean"
            errors =  address_data.errors

            return render(request, 'shopping/address.html', {'form': form, 'errors': errors}) 

    else:   
        form = AuthAddressForm(initial={
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
        })

        return render(request, 'shopping/address.html', {'form': form,})

def DiscountFindView(request):
    """
    this view will attempt to find a valid coupon and apply it to the current
    order.

    keyword arguments:
    name -- the name of the coupon the user is trying to apply to the order
    order_id -- the current active orders ID
    """

    name = request.POST.get('name')
    order_id = request.session['order_id']

    # change this key to be an environemnt variable in production
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

    order = stripe.Order.retrieve(order_id)
    discount_amount = ''
    
    # check to see if there is already a discount applied to this order
    for item in order['items']:
        if item['type'] == 'discount':
            return HttpResponse('Discount already applied')

    # attempt to retrieve coupon from stripe API
    try:
        coupon = stripe.Coupon.retrieve(name)

        # if there is a coupon add coupon to the order and save the order
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
        # if the coupon does not exist return the response
        # the response text (e.responseText) should say "No such coupon"
        return HttpResponse(e)

def CheckoutAddressDeleteView(request):
    """
    This view takes the pk of the address that the user wants deleted.
    After the address is deleted query for the remaining addresses,
    get the first address and make it the default address.
    If there is no address list it should go to the auth address view
    so the user can enter an address and continue to checkout

    args:
        pk: the pk of the address that the user wants deleted
        address: address object the user wants to delete
        user: current user
    """
    pk = request.POST.get('pk')
    address = Address.objects.get(id=pk)
    address.delete()    
    user = request.user

    try:
        # get the first adddress
        default_address = Address.objects.filter(email=user.email, address_type='shipping').first()
    except:
        default_address = None

    if default_address != None:
        Address.objects.filter(email=user.email, pk=default_address.id).update(default_address=True)

    return HttpResponse("address deleted sir")

def AddressChangeView(request):
    """
    view will allow user to update the default address to be used for orders.

    args:
        address_id = ID of the address the user has selected to be the default address. 
    """
    email = request.user.email
    address_id = request.POST.get('id')

    Address.objects.filter(email=email, address_type='shipping').update(default_address=False)
    Address.objects.filter(id=address_id).update(default_address=True)
    
    return HttpResponse('address changed')

def CheckOutAddressUpdateView(request, pk):

    """
    This view will allow the user to update already existing addresses associated
    to the user, add a new address, or delete exisiting addresses. View is 
    accessed from the checkout page
    
    Args:
        address: address that is being updated
        address_data: form data used to update an existing address object
        form: modelform that takes an instance of an exsiting address as an argument
        layout: the layout section of the form to modify the buttons

    """

    current_user = request.user

    if request.method == 'POST':

        address = Address.objects.get(id=pk)

        address_data = AuthAddressForm(request.POST, instance=address)

        address_data.save()

        return redirect(payment)

    else:

        address = Address.objects.get(id=pk)

        Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)
        Address.objects.filter(id=pk).update(default_address=True)

        form = AuthAddressForm(instance=address)

        form.helper.form_action = "/shopping/edit-address/%s/" % pk

        layout =  form.helper['layout'][1]
        layout[0].value = "Save changes"
        layout[1].html = "<a href='{% url 'update' %}' class='btn btn-default' id='cancel-button'> Cancel</a>"

        return render(request, 'shopping/address.html', {'form': form, 'pk':pk})

def StripePaymentView(request):

    """
    This is the view that will process the payment and send the user to the 
    order detail page. The token will be recieved from the stripe payment form.
    The order_id will be taken from the session variable. The order_id will
    be ue dto retrieve the stripe order_id. The token will then be used to 
    pay the for the retrieved stripe order. Once the payment is finished
    the cart is cleared.

    args:
        user: current user
        stripe.api_key: stripe apy key required to pay for order
        cart: cart for this session
        token: stripe token
        order_id: ID of current active order
        total: total amount of order
        item_total: total amount of items only
        
    """
    user = request.user 
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    cart = Cart(request.session)
    token = request.POST.get('stripeToken')
    if not 'order_id' in request.session:
        return redirect("/")
    else:
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

    cart.clear()
    del request.session['order_id']        

    context = {
        'order' : order,
        'item_count' : item_count,
        'total' : total,
        'tax_amount' : tax_amount,
        'shipping_amount' : shipping_amount,
        'item_total' : item_total,
        'discount_amount': discount_amount,
    }

    return render(request, 'shopping/order-summary.html', context)


def AddressView(request):
    """
    The user is directed to this view to create a new address from the 
    EditAuthCheckoutCheckoutAddress view. 

    args:
        user = current user
        form = model form
    """

    user = request.user

    form = AuthAddressForm(initial={
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
        })


    layout =  form.helper['layout'][1]
    layout[0].value = "Create address"
    layout[1].html = "<a href='{% url 'update' %}' class='btn btn-default' id='cancel-button'> Cancel</a>"

    return render(request, 'shopping/address.html', {'form': form,})    

@login_required(login_url='/accounts/login/')
def AddNewAddressView(request):
    """
    this is the view that that the user will visit with a new form so they can add a new shipping address

    on post they will create a new address and be redirected to their shipping list page from their profile
    """

    user = request.user

    if request.method == 'POST':
        form = AuthAddressForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('shipping')
    else:

        form = AuthAddressForm(initial={
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
        })

        form.helper.form_action ='add-new-address'

        layout =  form.helper['layout'][1]
        layout[0].value = "Save changes"
        layout[1].html = "<a href='{% url 'update' %}' class='btn btn-default' id='cancel-button'> Cancel</a>"

        return render(request, 'shopping/address.html', {'form' : form})


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


@login_required(login_url='/accounts/login/')
def ShippingView(request):

    """
    display all the addresses associated to the currently 
    logged in user. Page is accessed from their profile page.

    args:   
        user: currently logged in user
        address_list = all addressess associated to the user
    """

    user = request.user
    address_list = Address.objects.filter(email=user.email, address_type='shipping')

    return render(request, 'shopping/shipping.html', {'address_list': address_list}) 

@login_required(login_url='/accounts/login/')
def OrdersView(request):
    """
    This is the view that will display all of the current logged in users past orders

    args:
        user: current user
        stripe.api_key: key for stripe API.
        user_orders: past orders of user.
        stripe_orders: list of orders retrieved from stripe API
                       using the ID's in user_orders to make
                       the query.
        order_details: the details of the past order to be displayed
                       to the user.

    TODO:
        change user_orders to query orders based off of user ID
    """
    user = request.user

    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

    # retrieve all orders associate to this users email
    # should probably change this to using the user ID
    # they could change their email, that will be trouble
    user_orders = Order.objects.filter(email=user.email)

    #list of order id's
    orders = [str(order.order_id) for order in user_orders]

    #retrieve orders from stripe using the list of order ID's associated to user
    stripe_orders = stripe.Order.list(ids=orders)

    # order details list to use for iteration in the template
    order_details = [
        {
            'order_id' : str(order.id),
            'amount' : decimal.Decimal(order.amount) / 100,
            'order_created' : time.strftime('%Y-%m-%d', time.localtime(order.created)),
            'shipping' : order.shipping,
            'items' : [item.description for item in order['items'] if item.type=='sku'],
            'order_status' : order.status.title()
        }
        for order in stripe_orders
    ]

    return render(request, 'shopping/past-orders.html', {"order_details": order_details,})

@login_required(login_url='/accounts/login/')
def OrderDetailView(request, pk):
    """
    this is the view that will take the id of the stripe order and provide 
    information regarding only this specific order.
    """

    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"
    
    o = stripe.Order.retrieve(pk)
    order = {
            'order_id' : str(o.id),
            'amount' : decimal.Decimal(o.amount) / 100,
            'order_created' : time.strftime('%Y-%m-%d', time.localtime(o.created)),
            'shipping' : o.shipping,
            'items' : [item.description for item in o['items'] if item.type=='sku'],
            'order_status' : o.status.title()
        }

    return render(request, 'shopping/order-detail.html', {'order' : order})

@login_required(login_url='/accounts/login/')
def ProfileView(request):
    user = request.user

    return render(request, 'shopping/profile.html', {"user":user})

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


def StripeUpdateOrderView(request):
    """
    This view will update the order to reflect the shipping method
    that has been selected by the user

    args:
        order_id: order of the ID to be modified
        order: stripe order to be modified
        shipping_method: the ID of the shipping method selected
    """
    stripe.api_key = "sk_test_dMMQoiznhYQ9CeJJQp4YzdaT"

    order = stripe.Order.retrieve(request.POST.get('order_id'))
    
    order.selected_shipping_method = request.POST.get('shipping_method_id')

    order.save()

    shipping_price = [item.amount for item in order['items'] if item.type == 'shipping']

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
    This is the view that takes the authenticated user to the addresses on file from the payment page.
    if the user deletes all addresses they will be redirected to the create addresss view.

    args:
        user: current logged in user
        address_list: all addresses associated to the user
    """
    user = request.user

    address_list = Address.objects.filter(email=user.email, address_type='shipping')

    if len(address_list) == 0:
        return redirect("create-address")

    return render (request, 'shopping/select-shipping-address.html', {'address_list': address_list,})


def EditExistingAddressView(request, pk):

    """
    View will take the ID of the existing address the user wants to edit and
    get that address object. On post, update the existing address with the form 
    data supplied by the user and redirect to the view that displays all the
    addresses. On get display form to update the address the user selected to edit.

    args:
        user: current user
        address: address the user wants to edit
        address_list: addresses associated to the user
        form: Modeform for existing address object
        form.helper.form_action: sets the action of the form
        layout: class object to edit layout of form
        layout[1][0].value: Text on the save button of the form
        layout[1][1].html: change html of the cancel button to
                           take user back to ShippingView
    """
    user = request.user
    address = Address.objects.get(id=pk)

    if request.method == 'POST':
        form = AuthAddressForm(request.POST, instance=address)

        if form.is_valid():
            
            form.save()
            Address.objects.filter(id=pk).update(default_address=True)
            address_list = Address.objects.filter(email=current_user.email, address_type='shipping')

            return redirect('shipping')
    else:

        Address.objects.filter(email=user.email, address_type='shipping').update(default_address=False)
        Address.objects.filter(id=pk).update(default_address=True)

        form = AuthAddressForm(instance=address)
        form.helper.form_action ='add-new-address'

        layout = form.helper["layout"]
        layout.fields[0].legend = "Edit address"
        layout[1][0].value = "Save changes"
        layout[1][1].html = "<a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>"

        return render(request, 'shopping/address.html', {'form': form, })

@login_required(login_url='/accounts/login/')
def AddNewAddressView(request):
    """
    this is the view that that the user will visit with a new form so they can add a new shipping address

    on post they will create a new address and be redirected to their shipping list page from their profile

    on get it will display a form to create a new address
    """

    user = request.user
    if request.method == 'POST':
        form = AuthAddressForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('shipping')
    else:

        form = AuthAddressForm(initial={
            'first_name' : request.user.first_name,
            'last_name' : request.user.last_name,
            'email' : request.user.email,
        })

        return render(request, 'shopping/address.html', {'form' : form})

