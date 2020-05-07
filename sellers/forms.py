from django import forms
from .models import Seller

class SellerForm(forms.ModelForm):
    field_order = ['name', 'country', 'province', 'city', 'address', 'phone', 'web_address']
    class Meta:
        model = Seller
        fields = {'name', 'country', 'province', 'city', 'address', 'phone', 'web_address'}
