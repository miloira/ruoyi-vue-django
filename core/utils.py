import json
from functools import wraps

from django.http import HttpResponse, JsonResponse
from rest_framework.views import exception_handler

from core.models import SysUserRole, SysRoleMenu
from openpyxl import Workbook
from urllib.parse import quote

def is_admin(user):
    return SysUserRole.objects.filter(user_id=user.user_id, role_id=1).exists()

def get_perms(user):
    if is_admin(user):
        permissions = ['*:*:*']
    else:
        role_menus = SysRoleMenu.objects.filter(role_id__in=[obj.role_id for obj in user.roles.all()])
        permissions = [role_menu.menu.perms for role_menu in role_menus]
    return permissions

def has_permi(perms):
    def decorator(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            user = self.request.user
            if not is_admin(user):
                # 用户状态正常
                if user.status == '0':
                    roles = user.roles.filter(sysmenu__perms=perms, status='0')
                    # 角色正常且拥有权限
                    if roles:
                        return f(self, *args, **kwargs)
                    else:
                        res = {
                            'code': 500,
                            'msg': '没有操作权限'
                        }
                        return JsonResponse(res)
                else:
                    res = {
                        'code': 500,
                        'msg': '账户已停用'
                    }
                    return JsonResponse(res)
            else:
                return f(self, *args, **kwargs)
        return wrapper
    return decorator

def gen_routers(menu_list_top, menu_list):
    """
    前端左侧的路由菜单栏
    """

    def is_hidden(menu):
        return True if (menu.get("visible") == "1") else False

    def get_children(menu):
        current_menu_id = menu.get("menu_id")
        c_menu = []
        for item in menu_list:
            if item.get("parent_id") == current_menu_id:
                c_menu.append(item)
            else:
                pass
        return c_menu

    def build_menus_func(menu_li):
        routers = []
        for menu in menu_li:
            # 如果他是一个链接
            #  目录
            if menu.get("menu_type") == "M":

                if 0 == menu.get("is_frame"):
                    router = {
                        "name": menu.get("menu_name"),
                        "path": menu.get("path"),
                        "hidden": is_hidden(menu),
                        "component": None,
                        "meta": {
                            "title": menu.get("menu_name"),
                            "icon": menu.get("icon"),
                            "noCache": True,
                            "link": menu.get("path"),
                        },
                    }
                    routers.append(router)
                else:
                    if menu.get("parent_id") == 0:
                        router = {
                            "name": menu.get("component_name"),
                            "path": "/" + menu.get("path"),
                            "hidden": is_hidden(menu),
                            "redirect": "noRedirect",
                            "component": "Layout",
                            "alwaysShow": True,
                            "meta": {
                                "title": menu.get("menu_name"),
                                "icon": menu.get("icon"),
                                "noCache": False,
                                "link": None,
                                "breadcrumb": menu.get("breadcrumb")
                            }
                        }
                    else:
                        router = {
                            "name": menu.get("component_name"),
                            "path": menu.get("path"),
                            "hidden": is_hidden(menu),
                            "redirect": "noRedirect",
                            "component": "ParentView",
                            "alwaysShow": True,
                            "meta": {
                                "title": menu.get("menu_name"),
                                "icon": menu.get("icon"),
                                "noCache": False,
                                "link": None,
                                "breadcrumb": menu.get("breadcrumb")
                            }
                        }
                    c_menus = get_children(menu)
                    router["children"] = build_menus_func(c_menus)
                    routers.append(router)

            # 菜单
            if menu.get("menu_type") == "C":
                if menu.get("parent_id") == 0:
                    router = {
                        "path": "/",
                        "hidden": is_hidden(menu),
                        "component": "Layout",
                        "meta": None
                    }
                    children_list = []
                    children = {
                        "name": menu.get("component_name"),
                        "path": menu.get("path"),
                        "component": menu.get("component"),
                        "hidden": is_hidden(menu),
                        "meta": {
                            "title": menu.get("menu_name"),
                            "icon": menu.get("icon"),
                            "noCache": menu.get("no_cache"),
                            "link": menu.get("path"),
                            "affix": menu.get("affix"),
                            "breadcrumb": menu.get("breadcrumb")
                        }
                    }
                    children_list.append(children)
                    router["children"] = children_list
                else:
                    router = {
                        "name": menu.get("component_name"),
                        "path": menu.get("path"),
                        "component": menu.get("component"),
                        "hidden": is_hidden(menu),
                        "meta": {
                            "title": menu.get("menu_name"),
                            "icon": menu.get("icon"),
                            "noCache": menu.get("no_cache"),
                            "link": menu.get("path"),
                            "affix": menu.get("affix"),
                            "breadcrumb": menu.get("breadcrumb")
                        },
                    }
                routers.append(router)
        return routers

    return build_menus_func(menu_list_top)

def get_label_tree(menu_list):
    """
    获取到菜单的树形结构
    """

    def get_children(menu):
        current_id = menu.get("id")
        c_menu = [item for item in menu_list if item.get("parent_id") == current_id]
        if c_menu:
            return c_menu
        else:
            pass

    def build_menu_func(menu_li):
        routers = []
        for menu in menu_li:
            router = {
                "id": menu.get("id"),
                "label": menu.get("label")
            }
            c_menus = get_children(menu)

            if c_menus:
                router["children"] = build_menu_func(c_menus)
            else:
                pass
            routers.append(router)
        return routers

    menu_list_top = [item for item in menu_list if item.get("parent_id") == 0]
    return build_menu_func(menu_list_top)

def export_table(filename,rows):
    response = HttpResponse(content_type='application/msexcel')
    response['Access-Control-Expose-Headers'] = f'Content-Disposition'
    response['Content-Disposition'] = f'attachment;filename={quote(filename)}'
    wb = Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    wb.save(response)

    return response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        # 定制表单验证错误时的响应
        if 'non_field_errors' in response.data:
            response.status_code = 200
            response.data['code'] = 500
            response.data['msg'] = response.data['non_field_errors'][0]
            del response.data['non_field_errors']
        elif 'detail' in response.data:
        # 定制JWT失效时的响应
            response.status_code = 200
            response.data['code'] = 401
            response.data['msg'] = response.data['detail']
            del response.data['detail']

    return response

def is_json(s):
    try:
        json.loads(s)
        return True
    except:
        return False