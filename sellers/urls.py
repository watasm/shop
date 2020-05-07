from django.urls import path
from . import views


app_name = 'sellers'

urlpatterns = [
    path('seller_registration/', views.seller_registration, name='seller_registration'),
]
