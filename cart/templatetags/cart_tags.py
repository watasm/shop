from django import template
from cart.forms import CartAddProductForm

register = template.Library()

@register.inclusion_tag('cart/item_form.html')
def show_item_form(quantity):
    cart_item_form = CartAddProductForm(initial={'update': True, 'quantity': quantity})
    return {'cart_item_form': cart_item_form}

@register.simple_tag
def show_discount(cart, coupon):
    return cart.get_discount(coupon)
