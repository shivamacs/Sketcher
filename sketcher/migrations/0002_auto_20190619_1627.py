# Generated by Django 2.2.2 on 2019-06-19 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sketcher', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='id',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=200, primary_key=True, serialize=False, unique=True),
        ),
    ]
