from django.forms import ModelForm , ModelChoiceField
from django import forms
from models import Address
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field, Button, HTML
from crispy_forms.bootstrap import FormActions

class AddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
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
                Field('default_address', id="shipping-default-address"),
                Field('brain_tree_code', id="shipping-brain-tree-code"),
            ),
            FormActions(
            Submit('save', 'Save shipping address'),
            HTML("<a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'AddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = "/shopping/address/"



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
            'brain_tree_code': forms.HiddenInput(),
    	}

class BillingAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BillingAddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
       
        self.helper.layout = Layout(
            Fieldset(
                'Enter billing address',
                Field('first_name',id = "billing-first-name"),
                Field('last_name', id="billing-last-name"),
                Field('street_address', id="billing-street-address"),
                Field('extended_address', id="billing-extended-address"),
                Field('city', id="billing-city"),
                Field('state', id="billing-state"),
                Field('zip_code', id="billing-zip"),
                Field('address_type', id="billing-type"),
                Field('email', id="billing-email"),
                Field('same', id="billing-same"),
                Field('default_address', id="billing-default-address"),
                Field('brain_tree_code', id="billing-brain-tree-code"),

            ),
            FormActions(
            Submit('save', 'Save billing address'),
            HTML("<a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>")
        )
        )

        # You can dynamically adjust your layout

        self.helper.form_id = 'BillingAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = '/shopping/billing/'

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
            'brain_tree_code': forms.HiddenInput(),
            'same': forms.HiddenInput(),
        }


class EditAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
       
        self.helper.layout = Layout(
            Fieldset(
                'Edit address',
                Field('first_name',id = "billing-first-name"),
                Field('last_name', id="billing-last-name"),
                Field('street_address', id="billing-street-address"),
                Field('extended_address', id="billing-extended-address"),
                Field('city', id="billing-city"),
                Field('state', id="billing-state"),
                Field('zip_code', id="billing-zip"),
                Field('address_type', id="billing-type"),
                Field('email', id="billing-email"),
                Field('same', id="billing-same"),
                Field('default_address', id="billing-default-address"),
                Field('brain_tree_code', id="billing-brain-tree-code"),
            ),
            FormActions(
            Submit('save', 'Save changes'),
            HTML("<button type='button' class='btn btn-danger' data-toggle='modal' data-target='#myModal'>Delete address</button>"),
            ),
        )

        # You can dynamically adjust your layout

        self.helper.form_id = 'BillingAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'

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
            'brain_tree_code': forms.HiddenInput(),
            'same' : forms.HiddenInput(),
        }





