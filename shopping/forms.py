from django.forms import ModelForm , ModelChoiceField
from django import forms
from models import Address
from django.utils.translation import ugettext_lazy as _


class AddressForm(ModelForm):
    class Meta:
    	model = Address
    	fields = '__all__'
    	labels = {
    		'same': _("Billing same as Shipping"),
    		'street_address': _("Address"),
    		'extended_address': _("Address Line 2 (optional)"),
    	}
    	widgets = {
    		'email': forms.HiddenInput(),
    		'address_type': forms.HiddenInput(),
            'default_address': forms.HiddenInput(),
            'brain_tree_code': forms.HiddenInput(),
    	}



class BillingAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'street_address': _("Address"),
            'extended_address': _("Address Line 2 (optional)"),
        }
        widgets = {
            'email': forms.HiddenInput(),
            'address_type': forms.HiddenInput(),
            'default_address': forms.HiddenInput(),
            'same': forms.HiddenInput(),
        }