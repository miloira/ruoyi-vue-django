# Generated by Django 3.2.9 on 2022-04-22 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_sysloginlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysmenu',
            name='component_name',
            field=models.CharField(default=None, max_length=256, null=True, verbose_name='组件名称'),
        ),
    ]