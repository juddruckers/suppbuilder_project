from django.conf.urls import	include, url


from . import views 


urlpatterns = [
    url(r'^add/$', views.add, name='shopping-cart-add'),
    url(r'^remove/$', views.remove, name='shopping-cart-remove'),
    url(r'^delete/$', views.removeSingle, name='single-item-remove'),
    url(r'^show/$', views.show, name='shopping-cart-show'),
    url(r'^checkout/$', views.payment_view, name='checkout-view'),
    url(r'^order$', views.ThanksView, name='order-summary'),
    url(r'^order-detail$', views.OrderDetailView, name='order-detail'),
    url(r'^address/$', views.AddressView, name='address'),
    url(r'^billing/$', views.BillingAddressView, name='billing'),
    url(r'^shipping/$', views.ShippingView, name='shipping'),
    url(r'^change/$', views.AddressChangeView, name='address-change'),
    url(r'^update/(?P<pk>\d+)/$', views.AddressUpdateView, name='update'),
    url(r'^remove-address/(?P<pk>\d+)/$', views.AddressDeleteView, name='address-delete'),

]