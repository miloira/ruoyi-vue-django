# Generated by Django 3.2.9 on 2022-04-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_sysoperationlog_json_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysoperationlog',
            name='method',
            field=models.TextField(default=None, verbose_name='操作方法'),
        ),
    ]
