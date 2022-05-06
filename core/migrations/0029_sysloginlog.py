# Generated by Django 3.2.9 on 2022-04-22 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_sysoperationlog_request_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysLoginLog',
            fields=[
                ('create_by', models.CharField(blank=True, max_length=256, null=True, verbose_name='创建者')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('update_by', models.CharField(blank=True, max_length=256, null=True, verbose_name='更新者')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除')),
                ('info_id', models.AutoField(primary_key=True, serialize=False, verbose_name='日志编号')),
                ('username', models.CharField(max_length=256, verbose_name='用户名称')),
                ('ip_addr', models.GenericIPAddressField(verbose_name='登录地址')),
                ('login_location', models.CharField(max_length=512, verbose_name='登录地点')),
                ('browser', models.CharField(max_length=512, verbose_name='浏览器')),
                ('os', models.CharField(max_length=512, verbose_name='操作系统')),
                ('status', models.CharField(choices=[('0', '成功'), ('1', '失败')], max_length=1, verbose_name='状态')),
                ('msg', models.TextField(null=True, verbose_name='操作信息')),
                ('login_time', models.DateTimeField(auto_now_add=True, verbose_name='登录时间')),
            ],
            options={
                'verbose_name': '登录日志表',
                'db_table': 'sys_login_log',
            },
        ),
    ]
