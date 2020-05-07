from django import forms
from .models import SellerCoupon

class CouponApplyForm(forms.Form):
    code = forms.CharField()
