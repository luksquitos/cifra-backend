# Generated by Django 5.1 on 2025-05-29 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_rename_better_store_userlist_best_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlist',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Valor do produto no melhor local de compra', max_digits=12, null=True, verbose_name='Preço total'),
        ),
        migrations.AddField(
            model_name='productlist',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Valor total dos produtos do melhor local de compra baseado na quantidade', max_digits=12, null=True, verbose_name='Preço total'),
        ),
    ]
