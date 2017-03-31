from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_http_methods

from django.conf import settings
import braintree
import decimal
from allauth.account.forms import LoginForm
from carton.cart import Cart
from products.models import Product, Variation , Order
from shopping.models import Guest
from .models import Address
from .forms import AddressForm, BillingAddressForm, EditAddressForm
# Create your views here.


braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY)


def add(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('id'))
    cart.add(product, price=product.price)
    return render(request, 'shopping/show-cart.html')


def remove(request):
    cart = Cart(request.session)
    product_list = request.POST.getlist('delete_item_list[]')

    for item in product_list:
        product_id = int(item)
        product = Product.objects.get(id=product_id)
        cart.remove(product)
        
    return HttpResponse("Removed")


def removeSingle(request):
    cart = Cart(request.session)
    product_id = Product.objects.get(id=request.POST.get('product_id'))
    # item_id = str(Product.objects.get(id=request.GET.get('product_id')))
    print type(product_id)
    cart.remove(product_id)

    return HttpResponse("item removed")

def DiscountFindView(request):
    discount_list = braintree.Discount.all()
    name = request.GET.get('name')
    testvar = 'Invalid discount code'

    for discount in discount_list:
        if discount.name == name:
            testvar = discount.amount


        

    return HttpResponse(testvar)

def AddressDeleteView(request, pk):
    current_user_email = request.user.email
    current_user = request.user
    address = Address.objects.get(pk=pk);
    #delete that object
    Address.objects.filter(email=current_user_email, pk=pk).delete()
    #make every shipping address not the default
    Address.objects.filter(email=current_user_email, address_type='shipping').update(default_address=False)
    #get the list of existing addresses if there are any
    address_list = Address.objects.filter(email=current_user_email, address_type='shipping')

    try:
        braintree.Address.delete(str(current_user.id), str(address.brain_tree_code))
        print "deleting braintree address"
    except braintree.exceptions.not_found_error.NotFoundError as e:
        print "deleting address was unsuccessful"
    """
    If the length of the address is > 0 set the first address in the list as the default address then go back
    to the address list page. If the length of the list is !> 0 then redirect to the address form page
    """

    if len(address_list) > 0:
        #get the first items id.
        shipping_address = address_list[0].id

        #update that item to be the default address

        Address.objects.filter(email=current_user_email, address_type='shipping', id=shipping_address).update(default_address=True)

        return render(request, 'shopping/shipping.html', {'address_list': address_list, 'current_user': current_user})
    else:
        print "there is no address_list"
        return render(request, 'shopping/address.html', {'form': AddressForm}) 


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
    address = Address.objects.get(id=pk)

    if request.method == 'POST':

        updated_address = AddressForm(request.POST)
        if updated_address.is_valid():

            print "this was a post request"
            Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)
            Address.objects.filter(email=current_user.email, address_type='shipping', id=pk).update(default_address=True)


            address = Address.objects.update_or_create(
                        pk=pk,
                        defaults ={
                            'first_name' : updated_address.cleaned_data['first_name'],
                            'last_name' : updated_address.cleaned_data['last_name'],
                            'street_address' : updated_address.cleaned_data['street_address'],
                            'extended_address' : updated_address.cleaned_data['extended_address'],
                            'city' : updated_address.cleaned_data['city'], 
                            'state' : updated_address.cleaned_data['state'],
                            'zip_code' : updated_address.cleaned_data['zip_code'],
                            'email' : updated_address.cleaned_data['email'],
                            'address_type' : updated_address.cleaned_data['address_type'],
                            'default_address' : True,
                            'brain_tree_code' : updated_address.cleaned_data['brain_tree_code'],
                        }
                    )

            try:
                braintree.Address.update(str(current_user.id), str(updated_address.cleaned_data['brain_tree_code']),{
                    'first_name' : str(updated_address.cleaned_data['first_name']),
                    'last_name' : str(updated_address.cleaned_data['last_name']),
                    'street_address' : str(updated_address.cleaned_data['street_address']),
                    'extended_address' : str(updated_address.cleaned_data['extended_address']),
                    'locality' : str(updated_address.cleaned_data['city']),
                    'region': str(updated_address.cleaned_data['state']), 
                    'postal_code' : str(updated_address.cleaned_data['zip_code']),
                    'country_code_alpha2' : 'US',
                })
                print "updating braintree address"
            except braintree.exceptions.authorization_error.AuthorizationError as e:
                print e


            cart = Cart(request.session)
            cart_count = 0
            
            for product in cart.products:
                cart_count +=1

            token = braintree.ClientToken.generate({"customer_id": current_user.id})
            shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping', default_address=True).first()
            cart_total = cart.total + decimal.Decimal("4.99")
            
            context = {
                'token': token,
                'shipping_address': shipping_address,
                'cart_count' : cart_count,
                'cart_total' : cart_total
            }


            return render(request, 'shopping/payment_template.html', context)

    else :
        print " this was a get"
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
                'address_type' : address.address_type,
                'default_address' : address.default_address,
                'brain_tree_code' : address.brain_tree_code,
            })
        
        pk = Address.objects.get(id=pk)

        return render(request, 'shopping/address_form.html', {'form': existing_address_form, 'address': address, 'pk':pk})


def show(request):
    return render(request, 'shopping/show-cart.html')
    

def payment_view(request):


    
    if request.method == 'POST':

        cart = Cart(request.session)
        hidden_shipping = decimal.Decimal(request.POST['hidden_shipping'])

        payment_method_nonce = request.POST["payment_method_nonce"]
        discount = decimal.Decimal(request.POST['hidden_discount']) 
        discount_code = request.POST['discount_name']
        customer_id = str(request.user.id)
        discount_amount = decimal.Decimal("{0:.2f}".format(round(cart.total * discount,2)))
        order_total = (hidden_shipping + cart.total) - discount_amount



        if request.user.is_anonymous:
            guest = Guest.objects.get(email=request.session.get('email'))
            customer_id = str(guest.id)
            # query the guest_objects using the session variable
            #get the match and use the id in the transaction for customer_id
            billing_address = Address.objects.filter(email=guest.email, address_type='billing', default_address=True).first()
            shipping_address = Address.objects.filter(email=guest.email, address_type='shipping', default_address=True).first()
            
            result = braintree.Transaction.sale({
                'amount': order_total,
                'payment_method_nonce': str(payment_method_nonce),
                'customer_id' : str(guest.id),
                'billing_address_id': str(billing_address.brain_tree_code),
                'shipping_address_id' : str(shipping_address.brain_tree_code),
                'tax_amount' : '3.78',
                'custom_fields': {
                    'shipping_price' : str(hidden_shipping),
                },

                'options' : {
                    'submit_for_settlement': True,
                    'store_in_vault_on_success' : True,
                    'add_billing_address_to_payment_method': True,
                },
            })               

            if result.is_success == True:
                cart = Cart(request.session)
                cart_count = 0
                transaction = result.transaction
                grand_total = (transaction.amount + decimal.Decimal(transaction.custom_fields['shipping_price']) + decimal.Decimal(transaction.tax_amount))

                for product in cart.products:
                    cart_count +=1

                order = Order(
                    transaction_id= transaction.id,
                    email= guest.email,
                    first_name = transaction.shipping_details.first_name,
                    last_name = transaction.shipping_details.last_name,
                    date_ordered = transaction.created_at,
                    total = cart.total,
                    shipping = hidden_shipping,
                    discount = discount,
                    discount_code = discount_code,
                    tax = 3.78
                )

                order.save()

                for product in cart.products:
                    order.product.add(product)
                    order.save()

                cart.clear()
                subject = "Thank you for your order from Suppbuilder!"
                message = "Here are your order details"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [str(guest.email)]




                send_mail(subject, message, from_email, recipient_list, fail_silently=True) 

                return render(request, 'shopping/order-summary.html', {"order" : order, "transaction" : transaction, 'grand_total' : grand_total, 'cart_count': cart_count})
            
            elif result.is_success == False:

                print result.errors.deep_errors
                token = braintree.ClientToken.generate({"customer_id": guest.id})
                return render(request, 'shopping/payment_template.html', {"token": token, "shipping_address": shipping_address,})

            else:

                token = braintree.ClientToken.generate({"customer_id": guest.id})
                return render(request, 'shopping/payment_template.html', {"token": token, "shipping_address" : shipping_address,})

        else:
            billing_address = Address.objects.filter(email=current_user.email, address_type='billing', default_address=True).first()
            shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping', default_address=True).first()
            result = braintree.Transaction.sale({
                'amount': order_total,
                'payment_method_nonce': str(payment_method_nonce),
                'customer_id' : customer_id,
                'billing_address_id': str(billing_address.brain_tree_code),
                'shipping_address_id' : str(shipping_address.brain_tree_code),
                'tax_amount' : '3.78',
                'custom_fields': {
                    'shipping_price' : str(hidden_shipping),
                },

                'options' : {
                    'submit_for_settlement': True,
                    'store_in_vault_on_success' : True,
                    'add_billing_address_to_payment_method': True,
                },
            })
        
            if result.is_success == True:
                cart = Cart(request.session)
                cart_count = 0
                transaction = result.transaction
                grand_total = (transaction.amount + decimal.Decimal(transaction.custom_fields['shipping_price']) + decimal.Decimal(transaction.tax_amount))

                for product in cart.products:
                    cart_count +=1

                order = Order(
                    transaction_id= transaction.id,
                    email= request.user.email,
                    first_name = transaction.shipping_details.first_name,
                    last_name = transaction.shipping_details.last_name,
                    date_ordered = transaction.created_at,
                    total = cart.total,
                    shipping = hidden_shipping,
                    discount = discount,
                    discount_code = discount_code,
                    tax = 3.78
                )

                order.save()

                for product in cart.products:
                    order.product.add(product)
                    order.save()

                cart.clear()
                subject = "Thank you for your order from Suppbuilder!"
                message = "Here are your order details"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [str(current_user.email)]




                send_mail(subject, message, from_email, recipient_list, fail_silently=True) 

                return render(request, 'shopping/order-summary.html', {"order" : order, "transaction" : transaction, 'grand_total' : grand_total, 'cart_count': cart_count})

            elif result.is_success == False:

                print result.errors.deep_errors
                token = braintree.ClientToken.generate({"customer_id": current_user.id})
                return render(request, 'shopping/payment_template.html', {"token": token, "shipping_address": shipping_address,})

            else:

                token = braintree.ClientToken.generate({"customer_id": current_user.id})
                return render(request, 'shopping/payment_template.html', {"token": token, "shipping_address" : shipping_address,})

    else:


        guest_email = request.session.get('email')


        # if the user is anonymous check the session variable guest email
        # if the guest email is none go to to the login page to either log in 
        # or continue as a guest and create the session variable       
        if request.user.is_anonymous:
            guest_email = request.session.get('email')
            print guest_email
            guest = Guest.objects.filter(email=guest_email).first() 
            
            if guest_email is None:

                form = LoginForm()
                return render(request, 'account/login.html', {'form' : form})

            #if the session test has an email available 
            else:
                print "user is anonymous but the session variable has his email"

                shipping_address = Address.objects.filter(email=guest_email, address_type='shipping', default_address='True').first()
                billing_address = Address.objects.filter(email=guest_email, address_type='shipping', default_address='True').first()


                if shipping_address is None:
                    return render(request, 'shopping/address.html', {'form': AddressForm,})

                if billing_address is None:
                    form = BillingAddressForm(initial={'address_type': 'billing'})
                    return render(request, 'shopping/billing_address.html', {'form': form})                    


                cart = Cart(request.session)
                cart_count = 0

                for product in cart.products:
                    cart_count +=1


                cart_total = cart.total + decimal.Decimal("4.99")

                # need to get the token using the guests email to get the braintree id

                guest = Guest.objects.filter(email=guest_email).first()
                print guest

                token = braintree.ClientToken.generate({"customer_id": str(guest.id)})

                context = {
                    'token': token,
                    'shipping_address': shipping_address,
                    'billing_address' : billing_address,
                    'cart_count' : cart_count,
                    'cart_total' : cart_total
                }
                
                return render(request, 'shopping/payment_template.html', context)

        if request.user.is_authenticated():

            # make sure that the logged in user has a billing and shipping address
            #get a list of addresses associated with the email
            billing_list = Address.objects.filter(email=request.user.email, address_type='billing', default_address=True)
            shipping_list = Address.objects.filter(email=request.user.email, address_type='shipping', default_address=True)

            
            if len(shipping_list) < 1:
                print "there is less than 1 shipping address available meaning none."
                return render(request, 'shopping/address.html', {'form': AddressForm,})
            elif len(billing_list) < 1:
                print "there is less than 1 billing address available"
                form = BillingAddressForm(initial={'address_type': 'billing'})
                return render(request, 'shopping/billing_address.html', {'form': form})  
            else: 

                cart = Cart(request.session)
                cart_count = 0
                
                for product in cart.products:
                    cart_count +=1


                cart_total = cart.total + decimal.Decimal("4.99")

                token = braintree.ClientToken.generate({"customer_id": current_user.id})

                single_billing = Address.objects.filter(email=request.user.email, address_type='billing', default_address=True).first()
                single_shipping = Address.objects.filter(email=request.user.email, address_type='shipping', default_address=True).first()
                
                context = {
                    'token': token,
                    'shipping_address': single_shipping,
                    'billing_address' : single_billing,
                    'cart_count' : cart_count,
                    'cart_total' : cart_total
                }




                return render(request, 'shopping/payment_template.html', context)



def AddressView(request):

    form = AddressForm()
    current_user = request.user
    customer_id = str(current_user.id)


    if request.user.is_anonymous:
        current_user = Guest.objects.get(email=request.session['email'])
        customer_id = current_user.id

    if request.method == 'POST':
          

        #create a form instance from POST data
        address_data = AddressForm(request.POST)

        if address_data.is_valid():

            #create but dont save new address instance
            shipping_address = address_data.save(commit=False)

            #modify email field to current logged in users email
            shipping_address.email = current_user.email

            #change all previously saved shipping addresses to a default address value of False

            Address.objects.filter(email=current_user.email, address_type='shipping').update(default_address=False)

            #create the braintree address using the user ID and take the brain tree address id
            #then save it to the address being created
            braintree_shipping_address = braintree.Address.create({
                'customer_id' : str(customer_id),
                'first_name' : str(address_data.cleaned_data['first_name']),
                'last_name' : str(address_data.cleaned_data['last_name']),
                'street_address' : str(address_data.cleaned_data['street_address']),
                'extended_address' : str(address_data.cleaned_data['extended_address']),
                'locality' : str(address_data.cleaned_data['city']),
                'region': str(address_data.cleaned_data['state']), 
                'postal_code' : str(address_data.cleaned_data['zip_code']),
                'country_code_alpha2' : 'US',

            })
            if braintree_shipping_address.is_success:
                print "braintree shipping address saved successfully and saving the braintree code to the shipping address"
                shipping_address.brain_tree_code = braintree_shipping_address.address.id
                shipping_address.save()
            else:
                print 'billing address has errors'
                print braintree_shipping_address.errors.deep_errors


      
            if shipping_address.same == True:
                print "make a new billing address"

                Address.objects.filter(email=current_user.email, address_type='billing').update(default_address=False)
                billing_address = Address.objects.get(pk=shipping_address.id)
                billing_address.pk = None
                billing_address.address_type = 'billing'
                billing_address.save()

                braintree_billing_address = braintree.Address.create({
                    'customer_id' : str(current_user.id),
                    'first_name' : str(billing_address.first_name),
                    'last_name' : str(billing_address.last_name),
                    'street_address' : str(billing_address.street_address ),
                    'extended_address' : str(billing_address.extended_address),
                    'locality' : str(billing_address.city),
                    'region': str(billing_address.state), 
                    'postal_code' : str(billing_address.zip_code),
                    'country_code_alpha2' : 'US',
                })

                if braintree_billing_address.is_success:
                    print "billing address saved successfully and saving the braintree code to the billing address"
                    billing_address.brain_tree_code = braintree_billing_address.address.id
                    billing_address.save()

                    cart = Cart(request.session)
                    cart_count = 0
                    
                    for product in cart.products:
                        cart_count +=1


                    cart_total = cart.total + decimal.Decimal("4.99")
                    print cart_total

                    token = braintree.ClientToken.generate({"customer_id": current_user.id})
                    billing_address = Address.objects.filter(email=current_user.email, address_type='billing', default_address='True').first()
                    shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping', default_address='True').first()

                    context = {
                        'token': token,
                        'shipping_address': shipping_address,
                        'billing_address' : billing_address,
                        'cart_count' : cart_count,
                        'cart_total' : cart_total
                    }

                    return render(request, 'shopping/payment_template.html', context)

                else:
                    print 'billing address has errors'
                    print braintree_shipping_address.errors.deep_errors
                    return render(request, 'shopping/address.html', {'form': AddressForm})
            else:
                billing_address = Address.objects.filter(email=current_user.email, address_type='billing', default_address=True).first()
                if billing_address == None:
                    print "going to create a billing address now"
                    form = BillingAddressForm(initial={'address_type': 'billing'})
                    return render(request, 'shopping/billing_address.html', {'form': form})
                else:
                    cart = Cart(request.session)
                    cart_count = 0
                    
                    for product in cart.products:
                        cart_count +=1

                    cart_total = cart.total + decimal.Decimal("4.99")
                    print cart_total

                    token = braintree.ClientToken.generate({"customer_id": current_user.id})
                    billing_address = Address.objects.filter(email=current_user.email, address_type='billing', default_address='True').first()
                    shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping', default_address='True').first()

                    context = {
                        'token': token,
                        'shipping_address': shipping_address,
                        'billing_address' : billing_address,
                        'cart_count' : cart_count,
                        'cart_total' : cart_total
                    }

                    return render(request, 'shopping/payment_template.html', context)

        else:
            print "data is not clean"
            errors =  address_data.errors
            return render(request, 'shopping/address.html', {'form': AddressForm, 'errors': errors}) 

    else:
        print 'no post data receieved'
            
        return render(request, 'shopping/address.html', {'form': AddressForm,})    



def BillingAddressView(request):
    form = BillingAddressForm()
    current_user = request.user
    customer_id = str(current_user.id)


    if request.user.is_anonymous:
        current_user = Guest.objects.get(email=request.session['email'])
        customer_id = current_user.id

    if request.method == 'POST':

        """
        create a new shipping address, find the braintree customer. If the braintree customer doesnt exist create it.
        """
          

        #create a form instance from POST data
        address_data = BillingAddressForm(request.POST)

        if address_data.is_valid():

            #create but dont save new address instance
            billing_address = address_data.save(commit=False)

            #modify email field to current logged in users email
            billing_address.email = current_user.email

            #change all previously saved billing addresses to a default address value of False

            Address.objects.filter(email=current_user.email, address_type='billing').update(default_address=False)

            #create the braintree address using the user ID and take the brain tree address id
            #then save it to the address being created
            braintree_billing_address = braintree.Address.create({
                'customer_id' : str(customer_id),
                'first_name' : str(request.POST['first_name']),
                'last_name' : str(request.POST['last_name']),
                'street_address' : str(request.POST['street_address']),
                'extended_address' : str(request.POST['extended_address']),
                'locality' : str(request.POST['city']),
                'region': str(request.POST['state']), 
                'postal_code' : str(request.POST['zip_code']),
                'country_code_alpha2' : 'US',

            })
            if braintree_billing_address.is_success:
                print "billing address saved successfully and saving the braintree code to the billing address"
                billing_address.brain_tree_code = braintree_billing_address.address.id            
                billing_address.save()
                token = braintree.ClientToken.generate({"customer_id": current_user.id})
                shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping', default_address=True).first()
                billing_address = Address.objects.filter(email=current_user.email, address_type='billing', default_address=True).first()

                cart = Cart(request.session)
                cart_count = 0
                
                for product in cart.products:
                    cart_count +=1

                cart_total = cart.total + decimal.Decimal("4.99")

                
                context = {
                    'token': token,
                    'shipping_address': shipping_address,
                    'billing_address' : billing_address,
                    'cart_count' : cart_count,
                    'cart_total' : cart_total
                }
                return render(request, 'shopping/payment_template.html', context)
            else:
                print 'billing address has errors'
                print braintree_billing_address.errors.deep_errors

        else:
            print "data is not clean"
            print address_data.errors
            return render(request, 'shopping/billing_address.html', {'form': BillingAddressForm}) 


    else:
        print 'no post data receieved'
        form = BillingAddressForm(initial={'address_type': 'billing'})
        return render(request, 'shopping/billing_address.html', {'form': form})    



@login_required(login_url='/accounts/login/')
@require_http_methods(["GET", "POST"])
def ShippingView(request):

    """
    This view will be the area the current logged in user will select their billing and shipping.
    We will get the email of the current_user and make a request to addresses filtered by the
    users email. We will then display the addresses with a choice to select or edit displayed
    billing and shipping addresses.

    """

    #retrieve the current users email


    current_user_email = request.user.email

    current_user = request.user

    address_list = Address.objects.filter(email=current_user_email, address_type='shipping')

    braintree_customer = braintree.Customer.find(str(current_user.id))
    # braintree_address = braintree.Address.find(current_user.id)
    print braintree_customer.addresses




    if address_list:
        print address_list
        return render(request, 'shopping/shipping.html', {'address_list': address_list, 'current_user': current_user})
    else:
        print "there is no address_list"
        return render(request, 'shopping/address.html', {'form': AddressForm})  
    

def OrdersView(request):

    current_user = request.user

    order = Order.objects.filter(email=request.user.email).order_by("-date_ordered")

    return render(request, 'shopping/past-orders.html', {"order": order,})

def OrderDetailView(request, id):

    current_user = request.user


    """
    -Use the pk from the request get the braintree transaction and use that same pk to get the order
    -display the shipping shipping information
    -display the billing information
    -display the payment method
    -display a list of the items
    -ability to add the item back to the cart
    -if the item is already in the cart do not display option to remove just state it is already in cart
    -modal to add item back into cart? add serving size 
    """

    product_count = 0

    transaction = braintree.Transaction.find(str(id))
    order = Order.objects.get(transaction_id=id)

    for product in order.product.all():
        product_count += 1

    print product_count
    grand_total = (transaction.amount + decimal.Decimal(transaction.custom_fields['shipping_price']) + decimal.Decimal(transaction.tax_amount))

    print grand_total
    context = {
        'transaction': transaction,
        'order' : order,
        'product_count' : product_count,
        'grand_total' : grand_total
    }


    return render(request, 'shopping/order-detail.html', context)

@login_required(login_url='/accounts/login/')
def ProfileView(request):
    current_user = request.user

    try:
        print 'attempting to find an existing braintree customer'
        customer = braintree.Customer.find(str(current_user.id))
        if customer:
            print 'found a fucking customah govenah'
    except braintree.exceptions.not_found_error.NotFoundError:
        print " No customer found, creating customer"
        result = braintree.Customer.create({
            'first_name' : current_user.first_name,
            'last_name' : current_user.last_name,
            "email" : current_user.email,
            "id" : current_user.id,
        })

        if result.is_success == True:
            customer = result.customer
            print "customer successfully created and printing ID"
        elif result.is_success == False:
            print result.errors.deep_errors
            print "customer not created"


    shipping_address = Address.objects.filter(email=current_user.email, address_type='shipping')


    print "printing address count below"



    context = {
        'current_user' : current_user,
        'customer': customer,
        'shipping_address' : shipping_address,
    }



    return render(request, 'shopping/profile.html', context)


@login_required(login_url='/accounts/login/')
def PaymentView(request):

    current_user = request.user
    customer = braintree.Customer.find(str(current_user.id))


    return render(request, 'shopping/payment-methods.html', {'customer' : customer})



def DeletePaymentView(request):

    token = str(request.POST['token'])


    current_user = request.user
    result = braintree.PaymentMethod.delete(token)

    if result.is_success:
        print "payment method deleted"
        return render(request, 'shopping/profile.html', {'current_user' : current_user})
    else:
        print "payment method not deleted"
        return render(request, 'shopping/payment-methods.html', {'customer' : customer})







