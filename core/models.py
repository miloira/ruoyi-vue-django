from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class BaseModel(models.Model):
    """
    模型基类
    """
    create_by = models.CharField(max_length=256, null=True, blank=True, verbose_name='创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_by = models.CharField(max_length=256, null=True, blank=True,  verbose_name='更新者')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        abstract = True

class SysDept(BaseModel):
    """
    部门表
    """
    dept_id = models.BigAutoField(primary_key=True, verbose_name='部门ID')
    parent_id = models.IntegerField(default=0, verbose_name='父部门ID')
    ancestors = models.CharField(max_length=128, null=True, default=None, verbose_name="祖级列表")
    dept_name = models.CharField(max_length=128, default=None, verbose_name="部门名称")
    order_num = models.IntegerField(default=0, verbose_name='显示顺序')
    leader = models.CharField(max_length=64, default=None, verbose_name='负责人')
    phone = models.CharField(max_length=64, default=None, verbose_name='联系电话')
    email = models.CharField(max_length=64, default=None, verbose_name='邮箱')
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default='0', verbose_name="部门状态")

    class Meta:
        db_table = 'sys_dept'
        verbose_name = '部门表'

class SysPost(BaseModel):
    """
    岗位表
    """
    post_id = models.BigAutoField(primary_key=True, verbose_name="岗位ID")
    post_code = models.CharField(max_length=64, verbose_name="岗位编码")
    post_name = models.CharField(max_length=64, verbose_name="岗位名称")
    post_sort = models.IntegerField(default=0, verbose_name="显示顺序")
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default='0', verbose_name='岗位状态')

    class Meta:
        db_table = 'sys_post'
        verbose_name = '岗位表'

class SysRole(BaseModel):
    """
    角色表
    """
    role_id = models.BigAutoField(primary_key=True, verbose_name='角色ID')
    role_name = models.CharField(max_length=64, default='common', verbose_name='角色名')
    role_key = models.CharField(max_length=64, default='common', verbose_name='角色权限字符')
    role_sort = models.IntegerField(default=-1, verbose_name='角色顺序')
    data_scope = models.CharField(max_length=1, choices=[('1', '全部数据权限'), ('2', '自定义数据权限'), ('3', '本部门数据权限'), ('4', '本部门及以下数据权限')], default=1, verbose_name='数据范围')
    dept_check_strictly = models.BooleanField(verbose_name="部门树选择项是否关联显示", default=True)
    menu_check_strictly = models.BooleanField(verbose_name="菜单树选择项是否关联显示", default=True)
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default='0', verbose_name='角色状态')

    depts = models.ManyToManyField(SysDept, related_name='roles', verbose_name='部门')

    class Meta:
        db_table = 'sys_role'
        verbose_name = '岗位表'

class SysMenu(BaseModel):
    """
    菜单表
    """
    menu_id = models.BigAutoField(primary_key=True, verbose_name='菜单ID')
    menu_name = models.CharField(max_length=64, verbose_name='菜单名称')
    parent_id = models.IntegerField(default=0, verbose_name='父菜单ID')
    order_num = models.IntegerField(default=0, verbose_name='显示顺序')
    path = models.CharField(max_length=256, null=True, default=None, verbose_name='路由地址')
    component = models.CharField(max_length=256, null=True, blank=True, default=None, verbose_name='组件路径')
    component_name = models.CharField(max_length=256, null=True, default=None, verbose_name='组件名称')
    menu_type = models.CharField(max_length=1, choices=[('M', '目录'), ('C', '菜单'), ('F', '按钮'), ('L', '外链')], verbose_name='菜单类型')
    visible = models.CharField(max_length=1, choices=[('0', '显示'), ('1', '隐藏')], default='0', verbose_name='菜单状态')
    perms = models.CharField(max_length=256, null=True, blank=True, default=None, verbose_name='权限标识')
    icon = models.CharField(max_length=256, default='#', verbose_name='菜单图标')
    is_frame = models.IntegerField(default=1, verbose_name='是否为外链（0是 1否）')
    no_cache = models.BooleanField(default=False, verbose_name='是否缓存')
    affix = models.BooleanField(default=False, verbose_name='是否固定')
    breadcrumb = models.BooleanField(default=True, verbose_name='是否在面包屑中显示')
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default=0, verbose_name='菜单状态')

    roles = models.ManyToManyField(SysRole, through='SysRoleMenu')

    class Meta:
        db_table = 'sys_menu'
        verbose_name = '菜单表'

class SysUser(BaseModel, AbstractUser):
    """
    用户表
    """
    user_id = models.BigAutoField(primary_key=True, verbose_name='用户ID')
    dept = models.ForeignKey(SysDept, default=1, on_delete=models.SET(1), verbose_name='部门')
    username = models.CharField(max_length=256, unique=True, verbose_name='用户账号')
    nickname = models.CharField(max_length=256, verbose_name='用户昵称')
    email = models.CharField(max_length=128, null=True, default=None, verbose_name='用户邮箱')
    phone_number = models.CharField(max_length=128, null=True, blank=False, verbose_name='手机号码')
    sex = models.CharField(max_length=1, choices=[('0', '男'), ('1', '女'), ('2', '未知')], default='2', verbose_name='用户性别')
    avatar = models.CharField(max_length=256, null=True, default=None, verbose_name='用户头像')
    password = models.CharField(max_length=512, verbose_name='用户密码')
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default='0', verbose_name='账号状态')
    login_ip = models.CharField(max_length=64, null=True, default=None, verbose_name='最后登录IP')
    login_date = models.DateTimeField(auto_now=True, verbose_name='最后登录时间')

    roles = models.ManyToManyField(SysRole, through='SysUserRole', verbose_name='角色')
    posts = models.ManyToManyField(SysPost, through='SysUserPost', verbose_name='岗位')

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户表'

class SysUserRole(models.Model):
    """
    角色用户表
    """
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, verbose_name="用户ID")
    role = models.ForeignKey(SysRole, on_delete=models.CASCADE, verbose_name="角色ID")

    class Meta:
        db_table = 'sys_user_role'
        verbose_name = '角色用户表'

class SysUserPost(models.Model):
    """
    用户岗位表
    """
    user = models.ForeignKey(SysUser, on_delete=models.CASCADE, verbose_name="用户ID")
    post = models.ForeignKey(SysPost, on_delete=models.CASCADE, verbose_name="岗位ID")

    class Meta:
        db_table = 'sys_user_post'
        verbose_name = '用户岗位表'

class SysRoleMenu(models.Model):
    """
    角色菜单表
    """
    role = models.ForeignKey(SysRole, on_delete=models.CASCADE, verbose_name="角色ID")
    menu = models.ForeignKey(SysMenu, on_delete=models.CASCADE, verbose_name="菜单ID")

    class Meta:
        db_table = 'sys_role_menu'
        verbose_name = '角色菜单表'

class SysDictType(BaseModel):
    """
    字典类型表
    """
    dict_id = models.AutoField(primary_key=True, verbose_name="字典主键")
    dict_name = models.CharField(max_length=64, default=None, verbose_name="字典名称")
    dict_type = models.CharField(max_length=64, default=None, verbose_name='字典类型')
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default='0', verbose_name='字典类型状态')

    def __str__(self):
        return self.dict_name

    class Meta:
        db_table = 'sys_dict_type'
        verbose_name = '字典类型表'

class SysDictData(BaseModel):
    """
    字典数据表
    """
    dict_code = models.AutoField(primary_key=True, verbose_name="主键")
    dict_sort = models.IntegerField(default=0, verbose_name="字典排序")
    dict_label = models.CharField(max_length=64, default=None,  verbose_name='字典标签')
    dict_value = models.CharField(max_length=1024, default=None, verbose_name="字典键值")
    dict_type = models.ForeignKey(SysDictType, on_delete=models.CASCADE, default=None, verbose_name='字典类型')
    css_class = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="样式属性（其他样式扩展）")
    list_class = models.CharField(max_length=64, default=None, verbose_name="表格回显样式")
    is_default = models.CharField(max_length=16, default='N', verbose_name="表格回显样式")
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '停用')], default='0', verbose_name='字典状态')

    class Meta:
        db_table = 'sys_dict_data'
        verbose_name = '字典数据表'

class SysConfig(BaseModel):
    """
    参数配置表
    """
    config_id = models.AutoField(primary_key=True, verbose_name='参数ID')
    config_name = models.CharField(max_length=32, verbose_name='参数名')
    config_key = models.CharField(max_length=128, verbose_name='参数的键')
    config_value = models.CharField(max_length=128, verbose_name='参数的值')
    config_type = models.CharField(max_length=1, default='Y', choices=[('Y', '是'), ('N', '否')],verbose_name='系统内置')

    class Meta:
        db_table = 'sys_config'
        verbose_name = '参数配置表'

class SysNotice(BaseModel):
    """
    通知公告表
    """
    notice_id = models.AutoField(primary_key=True, verbose_name='公告ID')
    notice_title = models.CharField(max_length=128, verbose_name='公告标题')
    notice_content = models.TextField(verbose_name='公告内容')
    notice_type = models.CharField(max_length=1, choices=[('1', '通知'), ('2', '公告')], verbose_name='公告类型')
    status = models.CharField(max_length=1, choices=[('0', '正常'), ('1', '关闭')], verbose_name='状态')

    class Meta:
        db_table = 'sys_notice'
        verbose_name = '通知公告表'

class SysOperationLog(BaseModel):
    """
    操作日志表
    """
    id = models.AutoField(primary_key=True, verbose_name='日志编号')
    title = models.CharField(max_length=512, verbose_name='系统模块')
    method = models.TextField(null=True,default=None, verbose_name='操作方法')
    business_type = models.CharField(max_length=32, verbose_name='操作类型')
    request_method = models.CharField(max_length=32, verbose_name='请求方式')
    request_url = models.TextField(null=True,default=None,verbose_name='请求url')
    request_param = models.TextField(verbose_name='请求参数')
    json_result = models.TextField(null=True, verbose_name='返回参数')
    error_msg = models.TextField(null=True, verbose_name='错误消息')
    ip = models.GenericIPAddressField(verbose_name='操作地址')
    location = models.CharField(max_length=512, verbose_name='操作地点')
    operator = models.CharField(max_length=256, verbose_name='操作人员')
    status = models.CharField(max_length=1, choices=[('0', '成功'), ('1', '失败')], verbose_name='状态')

    class Meta:
        db_table = 'sys_operation_log'
        verbose_name = '操作日志表'

class SysLoginLog(BaseModel):
    """
    登录日志
    """
    info_id = models.AutoField(primary_key=True, verbose_name='日志编号')
    username = models.CharField(max_length=256, verbose_name='用户名称')
    ip_addr = models.GenericIPAddressField(verbose_name='登录地址')
    login_location = models.CharField(max_length=512, verbose_name='登录地点')
    browser = models.CharField(max_length=512, verbose_name='浏览器')
    os = models.CharField(max_length=512, verbose_name='操作系统')
    status = models.CharField(max_length=1, choices=[('0', '成功'), ('1', '失败')], verbose_name='状态')
    msg = models.TextField(null=True, verbose_name='操作信息')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    class Meta:
        db_table = 'sys_login_log'
        verbose_name = '登录日志表'
        