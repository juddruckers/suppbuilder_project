from django.conf.urls import url


from . import views 

urlpatterns = [
    url(r'^energy/$', views.EnergyView, name='energy'),
    url(r'^energy-two/$', views.EnergyTwoView, name='energy-two'),
   	url(r'^vitamins/$', views.VitaminView, name='vitamin'),
   	url(r'^protein/$', views.ProteinView, name='protein'),
]