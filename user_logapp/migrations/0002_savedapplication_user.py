# Generated by Django 4.2.2 on 2023-09-23 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_logapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedapplication',
            name='user',
            field=models.ForeignKey(default=12345, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
