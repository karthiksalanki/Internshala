# Generated by Django 4.2.2 on 2023-09-27 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_logapp', '0003_alter_savedapplication_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internships',
            name='Experience',
        ),
    ]
