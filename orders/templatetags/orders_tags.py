from django import template

register = template.Library()

@register.simple_tag
def show_discount(order, coupon):
    return order.get_discount(coupon)
