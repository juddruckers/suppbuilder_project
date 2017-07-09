from django.conf.urls import url


from . import views 

urlpatterns = [
    url(r'^energy/$', views.EnergyView, name='energy'),
   	url(r'^vitamins/$', views.VitaminView, name='vitamin'),
   	url(r'^protein/$', views.ProteinView, name='protein'),
	url(r'^new-protein/$', views.NewProteinView, name='new-protein'),
	url(r'^protein-count/$', views.ProteinCount, name='protein-count'),
]