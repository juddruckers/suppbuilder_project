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
            ),
            FormActions(
            Submit('save', 'Proceed to checkout'),
            HTML("{% if request.user.is_authenticated %} <a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>{% endif %}")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'AddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = "/shopping/guest-address/"



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

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Where should we ship your supps?',
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
            HTML("{% if request.user.is_authenticated %} <a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>{% endif %}")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'AuthAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = "/shopping/address/"



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


class EditAuthAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAuthAddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Where should we ship your supps?',
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
            HTML("{% if request.user.is_authenticated %} <a href='{% url 'new-address' %}' class='btn btn-default' id='cancel-button'> Add new address</a>{% endif %}")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'EditAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'



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


# this is the form 
class EditAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditAddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
       
        self.helper.layout = Layout(
            Fieldset(
                'Edit address',
                Field('first_name',id = "shipping-first-name"),
                Field('last_name', id="shipping-last-name"),
                Field('street_address', id="shipping-street-address"),
                Field('extended_address', id="shipping-extended-address"),
                Field('city', id="shipping-city"),
                Field('state', id="shipping-state"),
                Field('zip_code', id="shipping-zip"),
                Field('address_type', id="shipping-type"),
                Field('email', id="shipping-email"),
            ),
            FormActions(
            Submit('save', 'Save changes'),
            ),
        )

        self.helper.form_id = 'EditAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = '/shopping/update/'

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

class NewAuthAddressForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewAuthAddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Where should we ship your supps?',
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
            HTML("{% if request.user.is_authenticated %} <a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>{% endif %}")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'AuthAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = "/shopping/new-address/"

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





class EditExistingAddressForm(ModelForm):
    """
    This is the form that the user visits from the profile page and they select edit address
    """
    def __init__(self, *args, **kwargs):
        pk = str(kwargs.pop('pk', None))
        super(EditExistingAddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
       
        self.helper.layout = Layout(
            Fieldset(
                'Edit address',
                Field('first_name',id = "shipping-first-name"),
                Field('last_name', id="shipping-last-name"),
                Field('street_address', id="shipping-street-address"),
                Field('extended_address', id="shipping-extended-address"),
                Field('city', id="shipping-city"),
                Field('state', id="shipping-state"),
                Field('zip_code', id="shipping-zip"),
                Field('address_type', id="shipping-type"),
                Field('email', id="shipping-email"),
            ),
            FormActions(
            Submit('save', 'Save changes'),
            ),
        )

        self.helper.form_id = 'EditAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = '/shopping/edit-existing-address/'+ pk + '/'

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
            'same' : forms.HiddenInput(),
        }


class CreateNewAddressForm(ModelForm):
    """
    this is the form that the user will visit when attempting to create a new shipping
    address from the shipping list view inside the profile 
    """
    def __init__(self, *args, **kwargs):
        super(CreateNewAddressForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                'Where should we ship your supps?',
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
            HTML("{% if request.user.is_authenticated %} <a href='{% url 'shipping' %}' class='btn btn-default' id='cancel-button'> Cancel</a>{% endif %}")
        )

        )
        # You can dynamically adjust your layout

        self.helper.form_id = 'AuthAddressForm'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.form_method = 'post'
        self.helper.form_action = "/shopping/add-address/"



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

