from django import forms
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from .models import Profiles
from datetime import datetime
#from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.password_validation import validate_password

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length = 100, required = True)
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    date_joined = forms.DateTimeField(widget = forms.HiddenInput, initial = datetime.now)
    field_order = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'date_joined']

    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'username', 'email', 'password', 'confirm_password', 'date_joined'}

    def clean(self):
        super(UserForm, self).clean()
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')

        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match")

        if not first_name.isalpha():
            self._errors['first_name'] = self.error_class(['Please enter correct first name. Use only alphabetical characters (a-z, A–Z)'])

        if not last_name.isalpha():
            self._errors['last_name'] = self.error_class(['Please enter correct last name. Use only alphabetical characters (a-z, A–Z)'])

        try:
            validate_password(password)
        except forms.ValidationError as e:
            self._errors['password'] = self.error_class(e)

        # return errors
        del self.cleaned_data['confirm_password']
        return self.cleaned_data



class ProfilesForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields=('image',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('email', 'first_name', 'last_name', 'username')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profiles
        fields=('image',)
