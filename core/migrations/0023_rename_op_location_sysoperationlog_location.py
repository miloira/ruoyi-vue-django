# Generated by Django 3.2.9 on 2022-04-21 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20220421_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sysoperationlog',
            old_name='op_location',
            new_name='location',
        ),
    ]