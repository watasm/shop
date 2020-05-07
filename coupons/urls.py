from django.urls import path
from . import views

app_name = 'coupons'

urlpatterns = [
    path('apply/', views.seller_coupon_apply, name='apply'),
    path('detach/<int:id>/', views.seller_coupon_detach, name='detach'),
]
