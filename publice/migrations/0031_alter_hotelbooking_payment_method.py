# Generated by Django 5.1 on 2024-12-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publice', '0030_delete_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelbooking',
            name='payment_method',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Esewa', 'Esewa')], max_length=200, null=True),
        ),
    ]
