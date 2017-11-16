from django.forms import ModelForm , ModelChoiceField
from django import forms
from models import Address, Guest
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, Button, HTML
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse

class AddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Enter shipping address',
                Field('first_name',id = "shipping-first-name",),
                Field('last_name', id="shipping-last-name"),
                Field('street_address', id="shipping-street-address"),
                Field('extended_address', id="shipping-extended-address"),
                Field('city', id="shipping-city"),
                Field('state', id="shipping-state"),
                Field('zip_code', id="shipping-zip"),
                Field('address_type', id="shipping-type"),
                Field('email', id="shipping-email"),
                Field('same', id="shipping-same"),
            ),
            FormActions(
            Submit('save', 'Proceed to checkout'),
            HTML("{% if request.user.is_authenticated %} <a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>{% endif %}")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'AddressForm'
        self.helper.form_class = 'form'
        self.helper.label_class = 'col-xs-4'
        self.helper.field_class = 'col-xs-6'
        self.helper.form_method = 'post'
        self.helper.form_action = "create-address"



    class Meta:
    	model = Address
    	fields = '__all__'
    	labels = {
    		'same': _("Billing same as Shipping"),
    		'street_address': _("Address"),
    		'extended_address': _("Address Line 2"),
    	}
    	widgets = {
    		'email': forms.HiddenInput(),
    		'address_type': forms.HiddenInput(),
            'default_address': forms.HiddenInput(),
    	}


class AuthAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthAddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class="form-horizontal"
        self.helper.form_id = 'AuthAddressForm'
        self.helper.form_method = 'POST'
        self.helper.form_action = "create-address"

        self.helper.layout = Layout(
            Fieldset(
                'Where should we ship your supplement stack?',
                Field('first_name',id = "shipping-first-name",),
                Field('last_name', id="shipping-last-name"),
                Field('street_address', id="shipping-street-address"),
                Field('extended_address', id="shipping-extended-address"),
                Field('city', id="shipping-city"),
                Field('state', id="shipping-state"),
                Field('zip_code', id="shipping-zip"),
                Field('address_type', id="shipping-type"),
                Field('email', id="shipping-email"),
                Field('default_address', id="shipping-default-address"),
            ),
            FormActions(
            Submit('save', 'Proceed to checkout'),
            HTML("<a href='{% url 'cart' %}' class='btn btn-default' id='cancel-button'> Back to cart</a>")
            )
        )


    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'street_address': _("Address"),
            'extended_address': _("Address Line 2"),
        }
        widgets = {
            'email': forms.HiddenInput(),
            'address_type': forms.HiddenInput(),
            'default_address': forms.HiddenInput(),
        }

class GuestForm(ModelForm):

    class Meta:
        model = Guest
        fields = '__all__'


