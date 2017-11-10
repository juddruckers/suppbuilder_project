from django.conf.urls import	include, url


from . import views 


urlpatterns = [
    url(r'^item/add$', views.add_item, name='add-item'),
    url(r'^item/remove/$', views.remove_item, name='remove-item'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^checkout/$', views.payment, name='payment'),
    url(r'^stripe-payment/$', views.StripePaymentView, name='stripe-payment-view'),
    url(r'^stripe-update-order/$', views.StripeUpdateOrderView, name='stripe-update-order-view'),
    url(r'^guest-address/$', views.StripeGuestAddressView, name='stripe-guest-address-view'),
    url(r'^address/$', views.StripeAddressView, name='stripe-address-view'),
    url(r'^edit-guest-address/$', views.EditGuestAddressView, name='edit-guest-address'),     
    url(r'^order$', views.OrdersView, name='past-orders'),
    url(r'^order-detail/(?P<pk>\d+)/$', views.OrderDetailView, name='order-detail'),
    url(r'^address-list/$', views.AddressView, name='address'),
    url(r'^shipping/$', views.ShippingView, name='shipping'),
    url(r'^change/$', views.AddressChangeView, name='address-change'),
    url(r'^profile/$', views.ProfileView, name='profile'),
    url(r'^edit/(?P<pk>\d+)/$', views.AddressUpdateView, name='edit'),
    url(r'^edit-address/(?P<pk>\d+)/$', views.CheckOutAddressUpdateView, name='edit-checkout-address'),
    url(r'^update/$', views.EditAuthCheckoutAddressView, name='update'),
    url(r'^remove-checkout-address/$', views.CheckoutAddressDeleteView, name='checkout-address-delete'),
    url(r'^discount/$', views.DiscountFindView, name='discount'),
    url(r'^new-address/$', views.NewAddressView, name='new-address'),
    url(r'^edit-existing-address/(?P<pk>\d+)/$', views.EditExistingAddressView, name='edit-existing-address'),
    url(r'^add-address/$', views.AddNewAddressView, name='add-new-address'), 

]