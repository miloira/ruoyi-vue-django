import json
from functools import wraps

from django.http import JsonResponse

from core.models import SysOperationLog
from core.utils import is_admin, is_json

operation_type_map = {
    'create': '1',
    'update': '2',
    'destroy': '3',
    'auth': '4',
    'export_xlsx': '5',
    'import_xlsx': '6',
    'force_exit': '7',
    'clean_all': '8'
}

module_map = {
    'UserView': '用户管理',
    'RoleView': '角色管理',
    'MenuView': '菜单管理',
    'DeptView': '部门管理',
    'PostView': '岗位管理',
    'DictTypeView': '字典管理',
    'DictDataView': '字典管理',
    'ConfigView': '参数设置',
    'NoticeView': '通知公告',
    'OperationLogView': '操作日志',
    'LoginLogView': '登录日志'
}

def log(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        title = module_map.get(self.__class__.__name__, '未知') + ' / ' + f.__doc__
        method = '%s.%s.%s' %(__name__, self.__class__.__name__, f.__name__)
        business_type = operation_type_map[f.__name__]
        request_url = self.request.META['PATH_INFO']
        request_method = self.request.method
        request_param = {
            'params': dict(self.request.query_params),
            'data': self.request.data
        }
        ip = self.request.META['REMOTE_ADDR']
        location = '未知'
        operator = self.request.user.username
        error_msg = None
        response = None
        try:
            response = f(self, *args, **kwargs)
            json_result = response.content.decode('unicode_escape') if response else None
            json_result = json_result if is_json(json_result) else '{}'
            SysOperationLog.objects.create(
                title=title,
                method=method,
                business_type=business_type,
                request_url=request_url,
                request_method=request_method,
                request_param=json.dumps(request_param, ensure_ascii=False),
                json_result=json_result,
                ip=ip,
                location=location,
                operator=operator,
                status='0',
                error_msg=error_msg
            )
        except Exception as e:
            error_msg = str(e)
            json_result = response.content.decode('unicode_escape') if response else None
            json_result = json_result if is_json(json_result) else '{}'
            SysOperationLog.objects.create(
                title=title,
                method=method,
                business_type=business_type,
                request_url=request_url,
                request_method=request_method,
                request_param=json.dumps(request_param, ensure_ascii=False),
                json_result=json_result,
                ip=ip,
                location=location,
                operator=operator,
                status='1',
                error_msg=error_msg
            )
            raise e
        return response
    return decorator

def monitor(cls):
    methods = operation_type_map.keys()
    for method in methods:
        if hasattr(cls, method):
            wrapped = log(getattr(cls, method))
            setattr(cls, method, wrapped)
    return cls

def has_permi(perms):
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            user = self.request.user
            if user.status == '0':
                if not is_admin(user):
                    # 角色正常且拥有权限
                    if user.roles.filter(sysmenu__perms=perms, status='0'):
                        return f(self, *args, **kwargs)
                    else:
                        res = {
                            'code': 500,
                            'msg': '没有操作权限'
                        }
                        return JsonResponse(res, json_dumps_params={'ensure_ascii': False})
                else:
                    return f(self, *args, **kwargs)
            else:
                res = {
                    'code': 500,
                    'msg': '账户已停用'
                }
                return JsonResponse(res, json_dumps_params={'ensure_ascii': False})
        return wrapper
    return decorator

def has_role(roles):
    def decorator(f):
        def wrapper(self, *args, **kwargs):
            user = self.request.user
            if not is_admin(user):
                # 拥有相应状态正常的角色
                if user.roles.filter(role_key__in=roles, status='0'):
                    return f(self, *args, **kwargs)
                else:
                    res = {
                        'code': 500,
                        'msg': '没有操作权限'
                    }
                    return JsonResponse(res, json_dumps_params={'ensure_ascii': False})
            else:
                return f(self, *args, **kwargs)
        return wrapper
    return decorator
