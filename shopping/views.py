from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import braintree
from .forms import AddressForm, BillingAddressForm
from django.conf import settings
from carton.cart import Cart
from products.models import Product, Variation 
from .models import Address

# Create your views here.


braintree.Configuration.configure(braintree.Environment.Sandbox,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY)


def add(request):
    cart = Cart(request.session)
    variation = Variation.objects.get(id=request.GET.get('id'))
    # product = Product.objects.get(id=request.GET.get('id'))
    cart.add(variation, price=variation.price)
    return render(request, 'shopping/show-cart.html')


def remove(request):
    cart = Cart(request.session)
    # product = Product.objects.get(id=request.GET.get('id'))
    variation = Variation.objects.get(id=request.GET.get('id'))
    cart.remove(variation)
    return HttpResponse("Removed")


def show(request):
    return render(request, 'shopping/show-cart.html')



@login_required(login_url='/accounts/login/')
@require_http_methods(["GET", "POST"])
def payment_view(request):

    """ 
    payment view. Get the current_user ID and pass it to the client token. This will
    allow for repeat customers to access payment methods they have utilized before on 
    the site. 

    NOTE: NEED TO ADD IN CURRENT USER ID LATER TO RETRIEVE PREVIOUS METHODS USED TO MAKE PAYMENTS

    """

    if request.method == 'POST':
        cart = Cart(request.session)
        """
        retreive payment method nonce from form and use it to create transaction

        FOR TESTING PURPOSES:
        nonce should be "fake-valid-nonce"
        """

        current_user = request.user
        payment_method_nonce = request.POST["payment_method_nonce"]

        customer_id = str(request.user.id)

        braintree_customer = braintree.Customer.find(customer_id)

        billing_address = Address.objects.get(email=current_user.email, address_type='billing', default_address='True')

        shipping_address = Address.objects.get(email=current_user.email, address_type='shipping', default_address='True')


        
        result = braintree.Transaction.sale({
            'amount': cart.total,
            'payment_method_nonce': 'fake-valid-nonce',
            'customer_id' : customer_id,
            'billing_address_id': str(billing_address.brain_tree_code),
            'shipping_address_id' : str(billing_address.brain_tree_code),

            'customer' : {
                'first_name' : str(current_user.first_name),
                'last_name' : str(current_user.last_name),
                'email' : str(current_user.email),
            },
            'options' : {
                'submit_for_settlement': True,
                'store_in_vault_on_success' : True,
            },
        })

        
        payment_method = braintree.PaymentMethod.create({
            'customer_id' : customer_id,
            'payment_method_nonce' : 'fake-valid-no-billing-address-nonce',
            'billing_address_id' : str(billing_address.brain_tree_code),
            'options' : {
                "make_default" : True,
                "fail_on_duplicate_payment_method" : True,
            },
        })

        print "checking to see if payment method was created"
        if payment_method.is_success == True:
            print "payment method successfully saved"
        else:
            print "payment method error"
            print payment_method.errors.deep_errors




        if result.is_success == True:

            transaction = result.transaction

            #check the status of the transaction
            print transaction.type
            print transaction.status

            context = {'order' : result}

            #empty the cart

            cart.clear()

            return render(request, 'shopping/order-summary.html', context)

        elif result.is_success == False:


            
            print result.errors.deep_errors
            token = braintree.ClientToken.generate()
            return render(request, 'shopping/payment_template.html', {"token": token})

        else:

            token = braintree.ClientToken.generate()
            return render(request, 'shopping/payment_template.html', {"token": token})

    else:

        """ request the customer and if the customer does not exist then create it """
        current_user = request.user
        customer_email = str(request.user.email)
        customer_id = str(request.user.id)
        customer_first_name = str(request.user.first_name)
        customer_last_name = str(request.user.last_name)


        try: 
            braintree_customer = braintree.Customer.find(customer_id)
        except:
            print "creating braintree customer"
            result = braintree.Customer.create({
                "first_name": customer_first_name,
                "last_name": customer_last_name,
                "email": customer_email,
                'id': customer_id,
            })

            if result.is_success == True:
                customer = result.customer
                print "customer successfully created and printing ID"
            elif result.is_success == False:
                print result.errors.deep_errors
                print "customer not created"



        token = braintree.ClientToken.generate({"customer_id": customer_id})
        return render(request, 'shopping/payment_template.html', {"token": token}) 





@require_http_methods(["POST"])
def create_purchase(request):
    """
    final step of the transaction. use braintree.Transaction.sale({})
    return object used to show details of order.
    """
    if request.method == 'POST':
        cart = Cart(request.session)
        """
        retreive payment method nonce from form and use it to create transaction

        FOR TESTING PURPOSES:
        nonce should be "fake-valid-nonce"
        """
        payment_method_nonce = request.POST['payment_method_nonce']


        sale = {
          'amount': '10.00',
          'payment_method_nonce': 'fake-valid-no-billing-address-nonce',
          'options': {
            'submit_for_settlement': True
          }
        }

        
        payment_result = braintree.Transaction.sale(sale)


        if payment_result.is_success is True:
            context = {'order' : result}
            return render(request, 'shopping/order-summary.html', context)

        else:
            print "payment not fucking working yet"
            token = braintree.ClientToken.generate()
            return render(request, 'shopping/payment_template.html', {"token": token})



@login_required(login_url='/accounts/login/')
def AddressView(request):


    current_user_id = str(request.user.id)
    current_user = request.user
    user_email = request.user.email
    post_data = request.POST.get


    if request.method == 'POST' and request.POST['address_type'] == 'shipping':

        """
        create a new shipping address, find the braintree customer. If the braintree customer doesnt exist create it.
        """


        #create a form instance from POST data
        address_data = AddressForm(request.POST)

        if address_data.is_valid():

            #create but dont save new address instance
            shipping_address = address_data.save(commit=False)

            #modify email field to current logged in users email
            shipping_address.email = current_user.email

            #change all previously saved shipping addresses to a default address value of False

            Address.objects.filter(email=user_email, address_type='shipping').update(default_address=False)

            #create the braintree address using the user ID and take the brain tree address id
            #then save it to the address being created
            braintree_shipping_address = braintree.Address.create({
                'customer_id' : str(current_user.id),
                'first_name' : str(current_user.first_name),
                'last_name' : str(current_user.last_name),
                'street_address' : str(post_data('street_address')),
                'extended_address' : str(post_data('extended_address')),
                'locality' : str(post_data('city')),
                'region': str(post_data('state')), 
                'postal_code' : str(post_data('zip_code')),
                'country_code_alpha2' : 'US',

            })
            if braintree_shipping_address.is_success:
                print "billing address saved successfully"
            else:
                print 'billing address has errors'
                print braintree_shipping_address.errors.deep_errors

            print type(braintree_shipping_address)


            shipping_address.brain_tree_code = braintree_shipping_address.address.id


            shipping_address.save()

            #create billing address if that option was selected on the form

            if shipping_address.same == True:
                print "looks like they are shipping to the same area they are billing"


                billing_address = Address.objects.get(pk=shipping_address.pk)
                billing_address.address_type = 'billing'
                billing_address.pk = None


                braintree_billing_address = braintree.Address.create({
                    'customer_id' : str(current_user.id),
                    'first_name' : str(current_user.first_name),
                    'last_name' : str(current_user.last_name),
                    'street_address' : str(post_data('street_address')),
                    'extended_address' : str(post_data('extended_address')),
                    'locality' : str(post_data('city')),
                    'region': str(post_data('state')), 
                    'postal_code' : str(post_data('zip_code')),
                    'country_code_alpha2' : 'US',
                })
                
                billing_address.brain_tree_code = braintree_billing_address.address.id

                billing_address.save()

                if braintree_billing_address.is_success:
                    print "billing address saved successfully"
                else:
                    print 'billing address has errors'
                    print braintree_billing_address.errors.deep_errors
            
            #create braintree customer or add address to existing braintree customer

            #find customer
            existing_customer = braintree.Customer.find(current_user_id)


            #if there isnt a customer create it
            if not existing_customer:
                
                print " No customer found, creating customer"
                #create customer
                new_customer = braintree.Customer.create({
                    "email" : current_user.email,
                    "id" : current_user.id,
                })

                if new_customer.is_success:
                    print "new customer created successfully"
                else:
                    print new_customer.errors.deep_errors
            else:
                print "braintree customer found"

            #if the shipping address and the billing address are the same then generate 
            # braintree token and send send that to the checkout view

            if shipping_address.same == True:
                token = braintree.ClientToken.generate()
                return render(request, 'shopping/payment_template.html', {"token": token})
            else:
                return render(request, 'shopping/billing_address.html', {'form': BillingAddressForm(initial={'address_type': 'billing'})}) 

        else:

            print "data is not clean"
            print address_data.errors
            return render(request, 'shopping/address.html') 

    elif request.method == 'POST' and request.POST['address_type'] == 'billing':

        #create a form instance from POST data
        billing_address = AddressForm(request.POST)

        if billing_address.is_valid():

            #create but dont save
            billing_address = billing_address.save(commit=False)

            #modify email field to current logged in users email
            billing_address.email = current_user.email

            #change all previously saved shipping addresses to a default address value of False

            Address.objects.filter(email=user_email, address_type='billing').update(default_address=False)
            

            braintree_billing_address = braintree.Address.create({
                'customer_id' : str(current_user.id),
                'first_name' : str(current_user.first_name),
                'last_name' : str(current_user.last_name),
                'street_address' : str(post_data('street_address')),
                'extended_address' : str(post_data('extended_address')),
                'locality' : str(post_data('city')),
                'region': str(post_data('state')), 
                'postal_code' : str(post_data('zip_code')),
                'country_code_alpha2' : 'US',
            })

            billing_address.brain_tree_code = braintree_billing_address.address.id

            billing_address.save()

            token = braintree.ClientToken.generate()
            return render(request, 'shopping/payment_template.html', {"token": token})
    else:
        print 'no post data receieved'
        return render(request, 'shopping/address.html', {'form': AddressForm})    




@login_required(login_url='/accounts/login/')
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

    address_list = Address.objects.filter(email=current_user_email)

    if address_list:
        print address_list
    else:
        print "there is no address_list"

 
    return render(request, 'shopping/shipping.html', {'address_list': address_list, 'current_user': current_user})


















