# Generated by Django 4.2.4 on 2023-08-24 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_car_catagory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='placed_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
