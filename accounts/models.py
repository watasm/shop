from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart
# Create your models here.

class Profiles(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profiles')
    image = models.ImageField('image', upload_to='app1/images', default='', blank=True)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['id']

    def __str__(self):
        return str(self.user)
