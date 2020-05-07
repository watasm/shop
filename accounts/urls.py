from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .views import userEdit, profile
from . import views

#app_name = 'accounts'

urlpatterns = [
    path('useredit/', userEdit, name='useredit'),
    path('profile/<int:id>/', profile, name='profile'),
    path('email_check', views.email_check, name='email_check'),
    url(r'^accounts/confirm-email/(?P<uuid>[a-z0-9\-]+)/', views.verify, name='verify'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('allauth.urls')),
]+  static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
