from django.core.mail import send_mail
from myshop.celery import app
from .models import Seller
from myshop.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
import logging
from django.urls import reverse

@app.task
def send_verification_email(seller_id):
    try:
        seller = Seller.objects.get(pk = seller_id)
        send_mail(
            'Verify your Shop account',
            'Follow this link to verify your account: '
            'http://127.0.0.1:8000%s' % reverse('verify', kwargs={'uuid': str(seller.verification_uuid)}),
            EMAIL_HOST_USER,
            [seller.user.email],
            fail_silently=False,
        )

    except Seller.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
