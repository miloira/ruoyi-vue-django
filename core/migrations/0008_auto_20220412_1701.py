# Generated by Django 3.2.9 on 2022-04-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_sysuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysuser',
            name='avatar',
            field=models.CharField(default=None, max_length=256, null=True, verbose_name='用户头像'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='email',
            field=models.CharField(default=None, max_length=128, null=True, verbose_name='用户邮箱'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='login_ip',
            field=models.CharField(default=None, max_length=64, null=True, verbose_name='最后登录IP'),
        ),
    ]
