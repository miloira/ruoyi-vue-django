# Generated by Django 3.2.9 on 2022-04-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20220418_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysmenu',
            name='affix',
            field=models.BooleanField(default=False, verbose_name='是否固定'),
        ),
    ]
