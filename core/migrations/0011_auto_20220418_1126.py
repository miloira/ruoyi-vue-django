# Generated by Django 3.2.9 on 2022-04-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20220415_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sysdept',
            name='ancestors',
            field=models.CharField(default=None, max_length=128, null=True, verbose_name='祖级列表'),
        ),
        migrations.AlterField(
            model_name='sysrole',
            name='depts',
            field=models.ManyToManyField(related_name='roles', to='core.SysDept', verbose_name='部门'),
        ),
    ]