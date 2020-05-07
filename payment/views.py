import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
from cart.models import Cart
from django.contrib.auth.decorators import login_required
#from cart.cart import Cart
from django.db import IntegrityError
from django.contrib import messages

@login_required
def payment_process(request):
    order = get_object_or_404(Order, id=request.session['order_id'])
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)

        # Check products availability
        items = order.items.all()
        for item in items:
            if item.product.quantity < item.quantity:
                messages.error(request, 'Purchase error. There is no so much {} in the store. There is only left {} item.'.format(item.product.name, item.product.quantity))
                return redirect('cart:cart_detail')

        # create and submit transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            for item in items:
                product = item.product
                product.quantity -= item.quantity
                product.purchased_quantity += item.quantity
                product.save(update_fields=['quantity' ,'purchased_quantity'])
                # try:
                #     product.save(update_fields=['quantity' ,'purchased_quantity'])
                # except IntegrityError:
                #     messages.error(request, 'Purchase error. There is no so much {} in the store. There is only left {} item.'.format(item.product.name, item.product.quantity))
                #     return redirect('cart:cart_detail')
                # except:
                #     messages.error(request, 'Undefined purchase error')
                #     return redirect('cart:cart_detail')

            #request.session['coupon_id'] = None

            send_payment_informatin(order)
            return redirect('payment:done')

        else:
            send_payment_informatin(order)
            # for item in order.items.all():
            #     product = item.product
            #     product.quantity += item.quantity
            #     product.purchased_quantity -= item.quantity
            #     product.save(update_fields=['quantity'])
            return redirect('payment:canceled')


    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(request,'payment/process.html', {'order': order, 'client_token': client_token})

@login_required
def payment_done(request):
    # if request.user.is_authenticated:
    cart = get_object_or_404(Cart, user=request.user)
    # else:
    #     cart = Cart(request)
    coupons = cart.coupons.only('active', 'cart')
    for coupon in coupons:
        coupon.active = False
        coupon.cart = None
        coupon.save(update_fields=['active', 'cart'])
    cart.clear()
    return render(request, 'payment/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

def send_payment_informatin(order):
    # create invoice e-mail
    subject = 'My Shop - Invoice no. {}'.format(order.id)
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])
    # generate PDF
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    # attach PDF file
    email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
    # send e-mail
    email.send()
