from django.urls import path, re_path

from core.views.config import ConfigView
from core.views.dict_data import DictTypeView, DictDataView
from core.views.dept import DeptView
from core.views.login import CaptchaView, LoginView, UserInfoView, RoutersView, LogoutView
from core.views.logininfor import LoginLogView
from core.views.menu import MenuView
from core.views.notice import NoticeView
from core.views.operlog import OperationLogView
from core.views.post import PostView
from core.views.profile import UserProfileView, UserProfilePasswordView
from core.views.role import RoleView
from core.views.server import ServerView
from core.views.user import UserView


urlpatterns = [
    # 基础功能
    path('captcha_image/', CaptchaView.as_view()),  # 获取验证码
    path('login/', LoginView.as_view()),  # 登录
    path('get_info/', UserInfoView.as_view()),  # 个人信息
    path('get_routers/', RoutersView.as_view()),  # 路由信息
    path('logout/', LogoutView.as_view()),  # 注销

    # 用户管理
    path('system/user/', UserView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 用户列表 新增用户 修改用户
    re_path('system/user/(?P<pk>\d[,\d]*)/', UserView.as_view({'get': 'retrieve', 'delete': 'destroy'})), # 用户详情 删除用户
    path('system/user/profile/', UserProfileView.as_view()),  # 基本资料
    path('system/user/profile/update_pwd/', UserProfilePasswordView.as_view()),  # 修改密码
    path('system/user/option/', UserView.as_view({'get':'option'})), # 岗位和角色选项
    path('system/user/change_status/', UserView.as_view({'put':'change_status'})), # 修改用户状态
    path('system/user/export/', UserView.as_view({'post':'export_xlsx'})), # 导出用户数据
    path('system/user/import/', UserView.as_view({'post':'import_xlsx'})), # 导入用户数据
    path('system/user/import_template/', UserView.as_view({'post':'import_template'})), # 导入用户数据
    path('system/user/reset_pwd/', UserView.as_view({'put':'reset_pwd'})), # 重置密码
    re_path('system/user/auth_role/(?P<pk>\d+)/', UserView.as_view({'get':'auth_role', 'put':'add_role'})), # 可分配角色 分配角色

    # 角色管理
    path('system/role/', RoleView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 角色列表 新增角色 修改角色
    re_path('system/role/(?P<pk>\d[,\d]*)/', RoleView.as_view({'get': 'retrieve', 'delete': 'destroy'})), # 角色详情 删除角色
    path('system/role/change_status/', RoleView.as_view({'put': 'change_status'})),  # 修改用户状态
    path('system/role/auth_user/allocated_list/', RoleView.as_view({'get':'allocated_list'})), # 已分配用户列表
    path('system/role/auth_user/unallocated_list/', RoleView.as_view({'get':'unallocated_list'})), # 未分配用户列表
    path('system/role/auth_user/cancel/', RoleView.as_view({'put':'cancel'})), # 取消授权角色
    path('system/role/auth_user/cancel_all/', RoleView.as_view({'put':'cancel_all'})), # 批量取消授权角色
    path('system/role/auth_user/select_all/', RoleView.as_view({'put':'select_all'})), # 授权角色
    path('system/role/data_scope/', RoleView.as_view({'put':'data_scope'})), # 数据权限
    path('system/role/export/', RoleView.as_view({'post':'export_xlsx'})), # 导出角色数据

    # 部门管理
    path('system/dept/', DeptView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),  # 部门列表 新增部门 修改部门
    re_path('system/dept/(?P<pk>\d+)/', DeptView.as_view({'get': 'retrieve', 'delete': 'destroy'})), # 部门详情 删除部门
    re_path('system/dept/exclude/(?P<pk>\d+)/', DeptView.as_view({'get':'exclude'})), # 排除结点的部门树
    path('system/dept/tree_select/', DeptView.as_view({'get': 'tree_select'})), # 部门树
    re_path('system/dept/role_dept_tree_select/(?P<pk>\d+)/', DeptView.as_view({'get':'role_dept_tree_select'})), # 角色部门树

    # 岗位管理
    path('system/post/', PostView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),  # 岗位列表 新增岗位 修改岗位
    re_path('system/post/(?P<pk>\d[,\d]*)/', PostView.as_view({'get': 'retrieve', 'delete': 'destroy'})),  # 岗位详情 删除岗位
    path('system/post/export/', PostView.as_view({'post': 'export_xlsx'})), # 导出岗位数据

    # 菜单管理
    path('system/menu/', MenuView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 菜单列表 新增菜单 修改菜单
    re_path('system/menu/(?P<pk>\d[,\d]*)/', MenuView.as_view({'get': 'retrieve', 'delete': 'destroy'})),  # 菜单详情 删除菜单
    path('system/menu/tree_select/', MenuView.as_view({'get':'tree_select'})), # 菜单树
    re_path('system/menu/role_menu_tree_select/(?P<pk>\d+)/', MenuView.as_view({'get':'role_menu_tree_select'})), # 角色菜单树

    # 数据字典
    path('system/dict/type/', DictTypeView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 字典类型列表 新增字典类型 修改字典类型
    re_path('system/dict/type/(?P<pk>\d[,\d]*)/', DictTypeView.as_view({'get': 'retrieve', 'delete': 'destroy'})),  # 字典类型详情 删除字典类型
    path('system/dict/type/export/', DictTypeView.as_view({'post': 'export_xlsx'})),  # 导出字典类型数据
    path('system/dict/data/', DictDataView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 字典数据列表 新增字典数据 修改字典数据
    re_path('system/dict/data/(?P<pk>\d[,\d]*)/', DictDataView.as_view({'get': 'retrieve', 'delete': 'destroy'})), # 字典数据详情 删除字典数据
    path('system/dict/data/export/', DictDataView.as_view({'post': 'export_xlsx'})),  # 导出字典类型数据
    re_path('system/dict/data/type/(?P<value>\w+)/', DictDataView.as_view({'get':'dict_data'})), # 字典数据

    # 参数设置
    path('system/config/', ConfigView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 参数设置列表 新增参数设置 修改参数设置
    re_path('system/config/(?P<pk>\d[,\d]*)/', ConfigView.as_view({'get':'retrieve', 'delete':'destroy'})), # 参数设置详情 删除参数设置
    re_path('system/config/configKey/(?P<key>.*?)/', ConfigView.as_view({'get': 'get_value'})),  # 获取参数设置键值
    path('system/config/refresh_cache/', ConfigView.as_view({'delete':'refresh_cache'})), # 刷新缓存
    path('system/config/export/', ConfigView.as_view({'post': 'export_xlsx'})),  # 导出参数设置数据

    # 通知公告
    path('system/notice/', NoticeView.as_view({'get': 'list', 'post': 'create', 'put': 'update'})), # 通知公告列表 新增通知公告 修改通知公告
    re_path('system/notice/(?P<pk>\d[,\d]*)/', NoticeView.as_view({'get': 'retrieve', 'delete': 'destroy'})), # 通知公告详情 删除通知公告

    # 操作日志
    path('monitor/operlog/', OperationLogView.as_view({'get':'list', 'delete':'clean_all'})), # 操作日志列表 清空操作日志
    re_path('monitor/operlog/(?P<pk>\d[,\d]*)/', OperationLogView.as_view({'delete':'destroy'})), # 删除操作日志
    path('monitor/operlog/export/', OperationLogView.as_view({'post':'export_xlsx'})), # 导出操作日志数据

    # 登录日志
    path('monitor/logininfor/', LoginLogView.as_view({'get': 'list', 'delete': 'clean_all'})),  # 登录日志列表 清空登录日志
    re_path('monitor/logininfor/(?P<pk>\d[,\d]*)/', LoginLogView.as_view({'delete': 'destroy'})),  # 删除登录日志
    path('monitor/logininfor/export/', LoginLogView.as_view({'post': 'export_xlsx'})),  # 导出登录日志数据

    # 服务监控
    path('monitor/server/', ServerView.as_view({'get': 'list'})),
]

