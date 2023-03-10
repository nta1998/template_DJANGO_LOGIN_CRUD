# Generated by Django 4.0.6 on 2023-02-28 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0005_alter_post_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='facebookUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.TextField(blank=True, max_length=500)),
                ('email', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='pic',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
