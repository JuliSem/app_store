# Generated by Django 4.2.15 on 2024-09-22 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Корзину', 'verbose_name_plural': 'Корзина'},
        ),
    ]
