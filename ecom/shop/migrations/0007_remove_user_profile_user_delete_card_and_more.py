# Generated by Django 4.0.5 on 2022-06-09 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Card',
        ),
        migrations.DeleteModel(
            name='User_Profile',
        ),
    ]
