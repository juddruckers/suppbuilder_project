from django.conf.urls import include, url
from django.contrib import admin

from . import views
app_name='suppbuilder'
urlpatterns = [
    url(r'^$', views.IndexView, name='home'),
    url(r'^guest/$', views.StripeGuestView, name='guest'),    
]
