# Generated by Django 4.0.6 on 2023-03-01 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_facebookusers_user_alter_facebookusers_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookusers',
            name='email',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='facebookusers',
            name='password',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
