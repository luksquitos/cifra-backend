# Generated by Django 5.1 on 2025-05-22 01:25

import core.validators.cnpj_validator
import django.db.models.deletion
import features.user.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0005_store_address_store_cnpj_store_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='about',
        ),
        migrations.AlterField(
            model_name='priceproducthistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='store',
            name='address',
            field=models.CharField(default='Núcleo de Peixoto, 48\nPousada Santo Antonio\n85444-460 da Paz de Minas / RN', max_length=256, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='store',
            name='cnpj',
            field=models.CharField(default='13.648.275/0001-88', max_length=18, validators=[core.validators.cnpj_validator.CNPJValidator()], verbose_name='CNPJ'),
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store', to=settings.AUTH_USER_MODEL, validators=[features.user.validators.validate_logistic], verbose_name='Lojista'),
        ),
    ]
