# Generated by Django 4.2.4 on 2023-08-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_is_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='clientImage'),
        ),
    ]
