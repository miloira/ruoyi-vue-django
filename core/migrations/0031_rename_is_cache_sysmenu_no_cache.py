# Generated by Django 3.2.9 on 2022-04-22 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_sysmenu_component_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sysmenu',
            old_name='is_cache',
            new_name='no_cache',
        ),
    ]
