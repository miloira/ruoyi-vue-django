# Generated by Django 3.2.9 on 2022-04-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20220420_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysNotice',
            fields=[
                ('create_by', models.CharField(blank=True, max_length=256, null=True, verbose_name='创建者')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_by', models.CharField(blank=True, max_length=256, null=True, verbose_name='更新者')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('notice_id', models.AutoField(primary_key=True, serialize=False, verbose_name='公告ID')),
                ('notice_title', models.CharField(max_length=128, verbose_name='公告标题')),
                ('notice_content', models.TextField(verbose_name='公告内容')),
                ('notice_type', models.CharField(choices=[('1', '通知'), ('2', '公告')], max_length=1, verbose_name='公告类型')),
                ('status', models.CharField(choices=[('0', '正常'), ('1', '停用')], max_length=1, verbose_name='状态')),
            ],
            options={
                'verbose_name': '通知公告表',
                'db_table': 'sys_notice',
            },
        ),
        migrations.AlterModelOptions(
            name='sysconfig',
            options={'verbose_name': '参数配置表'},
        ),
    ]
