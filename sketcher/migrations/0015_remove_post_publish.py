# Generated by Django 2.2.2 on 2019-06-29 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sketcher', '0014_post_publish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='publish',
        ),
    ]
