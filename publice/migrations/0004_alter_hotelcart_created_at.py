# Generated by Django 5.1 on 2024-09-15 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publice', '0003_hotelcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelcart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
