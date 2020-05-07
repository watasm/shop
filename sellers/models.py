from django.db import models
from django.contrib.auth.models import User
import uuid
from phone_field import PhoneField

# Create your models here.
class Seller(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    name=models.CharField(max_length=100, unique=True)
    country=models.CharField(max_length=100)
    province=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    address=models.CharField(max_length=200, unique=True)
    phone=PhoneField(help_text='Contact phone number')
    web_address=models.URLField(max_length=100, unique=True)
    is_verified = models.BooleanField('verified', default=False)
    verification_uuid = models.UUIDField('Unique Verification UUID', default=uuid.uuid4)

    class Meta():
        ordering=('id',)

    def __str__(self):
        return self.name
