# Generated by Django 2.2.3 on 2019-07-08 10:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200, unique=True)),
                ('phone', phone_field.models.PhoneField(help_text='Contact phone number', max_length=31)),
                ('web_address', models.URLField(max_length=100, unique=True)),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('verification_uuid', models.UUIDField(default=uuid.uuid4, verbose_name='Unique Verification UUID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
