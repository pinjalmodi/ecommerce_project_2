# Generated by Django 5.1.3 on 2024-11-12 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usertype',
            field=models.CharField(choices=[('seller', 'seller'), ('buyer', 'buyer')], max_length=100),
        ),
    ]
