from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, ButtonHolder, Field
from crispy_forms.bootstrap import FormActions, PrependedText



class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['first_name'] + self.cleaned_data['last_name']
        user.save()

    def __init__(self, *args, **kwargs):
    	super(SignupForm, self).__init__(*args, **kwargs)
    	self.helper = FormHelper()
    	self.helper.form_class = 'signup'
    	self.helper.form_id = 'signup_form'
    	self.helper.form_method = 'post'
    	self.helper.form_action = "/accounts/signup/"
    	self.helper.layout = Layout(
    		Field('first_name', placeholder='First Name'),
    		Field('last_name', placeholder='Last Name'),
    		Field('email'),
    		Field('password1'),
    		Field('password2'),

    		FormActions(
    			Submit('save', 'Sign in', css_class='btn btn-success')
    		)
    	)