from django import forms
from .models import Product, ProductReview


class ProductAddForm(forms.ModelForm):
    field_order = ['category', 'name', 'description', 'image', 'price', 'quantity']
    class Meta:
        model = Product
        fields = {'category', 'name', 'description', 'image', 'price','quantity'}

class ProductEditForm(forms.ModelForm):
    field_order = ['category', 'name', 'description', 'image', 'price','quantity', 'available']
    class Meta:
        model = Product
        fields = {'category', 'name', 'description', 'image', 'price', 'quantity','available'}

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = {'text'}
