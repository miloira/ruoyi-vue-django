# Generated by Django 3.2.9 on 2022-04-18 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20220418_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysmenu',
            name='menu_type',
            field=models.CharField(choices=[('M', '目录'), ('C', '菜单'), ('F', '按钮'), ('L', '外链')], max_length=1, verbose_name='菜单类型'),
        ),
        migrations.AlterField(
            model_name='sysmenu',
            name='path',
            field=models.CharField(default=None, max_length=256, null=True, verbose_name='路由地址'),
        ),
    ]
