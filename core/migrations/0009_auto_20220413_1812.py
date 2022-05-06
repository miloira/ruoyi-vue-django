# Generated by Django 3.2.9 on 2022-04-13 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220412_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysuser',
            name='dept',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.sysdept', verbose_name='部门'),
        ),
        migrations.AlterField(
            model_name='sysuser',
            name='phone_number',
            field=models.CharField(max_length=128, null=True, verbose_name='手机号码'),
        ),
    ]
