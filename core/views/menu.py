from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysMenu, SysRole
from core.serializers import SysMenuSerializer
from core.utils import get_label_tree

@monitor
class MenuView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:menu:list')
    def list(self, request):
        """菜单列表"""
        menu_name = request.query_params.get('menu_name')
        status = request.query_params.get('status')

        query_condition = {}
        if menu_name:
            query_condition['menu_name'] = menu_name
        if status:
            query_condition['status'] = status

        menus = SysMenu.objects.filter(**query_condition)
        serializer = SysMenuSerializer(menus, many=True)
        for menu in serializer.data:
            menu['children'] = []

        res = {
            'code': 200,
            'msg': 'ok',
            'data': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:menu:add')
    def create(self, request):
        """新增菜单"""
        request.data['create_by'] = request.user.username
        serializer = SysMenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:menu:edit')
    def update(self, request):
        """修改菜单"""
        request.data['update_by'] = request.user.username
        menu = SysMenu.objects.filter(menu_id=request.data.get('menu_id')).first()
        if menu:
            serializer = SysMenuSerializer(menu, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '菜单不存在'
            }
        return JsonResponse(res)

    @has_permi('system:menu:query')
    def retrieve(self, request, pk):
        """菜单详情"""
        try:
            menu = SysMenu.objects.get(pk=pk)
        except SysMenu.DoesNotExist:
            res = {
                'code': 500,
                'msg': '菜单不存在',
            }
            return JsonResponse(res)

        serializer = SysMenuSerializer(menu)
        res = {
            'code': 200,
            'msg': 'ok',
            'data': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:menu:remove')
    def destroy(self, request, pk):
        """删除菜单"""
        try:
            menu = SysMenu.objects.get(pk=pk)
        except SysMenu.DoesNotExist:
            res = {
                'code': 500,
                'msg': '菜单不存在',
            }
            return JsonResponse(res)

        menu.delete()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    def tree_select(self, request):
        """菜单树"""
        menus = SysMenu.objects.all()
        res_objects_list = [{"id": menu.menu_id, "label": menu.menu_name, "parent_id": menu.parent_id} for menu in menus]
        tree = get_label_tree(res_objects_list)
        res = {
            'code': 200,
            'msg': 'ok',
            'data': tree
        }
        return JsonResponse(res)

    def role_menu_tree_select(self, request, pk):
        """角色菜单树"""
        role = SysRole.objects.filter(role_id=pk).first()
        if not role:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
            return JsonResponse(res)

        menus = SysMenu.objects.all()
        res_objects_list = [{"id": menu.menu_id, "label": menu.menu_name, "parent_id": menu.parent_id} for menu in menus]
        tree = get_label_tree(res_objects_list)
        checked_keys = [menu.menu_id for menu in role.sysmenu_set.all()]
        res = {
            'code': 200,
            'msg': 'ok',
            'menus': tree,
            'checked_keys': checked_keys
        }
        return JsonResponse(res)
