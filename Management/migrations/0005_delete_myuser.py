# Generated by Django 4.2 on 2023-05-13 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Management', '0004_alter_user_email_alter_user_fname_alter_user_lname'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
