# Generated by Django 3.2.3 on 2021-07-23 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210722_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='extension',
        ),
        migrations.RemoveField(
            model_name='services',
            name='taille',
        ),
    ]