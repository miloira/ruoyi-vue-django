from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.models import SysRole, SysMenu, SysUser, SysUserRole, SysDept
from core.serializers import SysRoleSerializer, SysUserSerializer
from core.utils import export_table
from core.decorator import monitor, has_permi

@monitor
class RoleView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:role:list')
    def list(self, request):
        """角色列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        role_name = request.query_params.get('role_name')
        role_key = request.query_params.get('role_key')
        status = request.query_params.get('status')
        begin_time = request.query_params.get('params[beginTime]')
        end_time = request.query_params.get('params[endTime]')

        query_condition = {}
        if role_name:
            query_condition['role_name__contains'] = role_name

        if role_key:
            query_condition['role_key__contains'] = role_key

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        roles = SysRole.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(roles, page_size)
        roles = paginator.get_page(page_num)
        serializer = SysRoleSerializer(roles, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'total': paginator.count,
            'rows': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:role:query')
    def retrieve(self, request, pk):
        """角色信息"""
        try:
            role = SysRole.objects.get(pk=pk)
        except SysRole.DoesNotExist:
            res = {
                'code': 500,
                'msg': '角色不存在',
            }
            return JsonResponse(res)

        serializer = SysRoleSerializer(role)
        res = {
            'code': 200,
            'msg': 'ok',
            'data': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:role:add')
    def create(self, request):
        """新增角色"""
        request.data['create_by'] = request.user.username
        serializer = SysRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:role:edit')
    def update(self, request):
        """修改角色"""
        request.data['update_by'] = request.user.username
        menu_ids = request.data.get('menu_ids')
        role = SysRole.objects.filter(role_id=request.data.get('role_id')).first()
        # 添加角色菜单
        role.sysmenu_set.set(SysMenu.objects.filter(menu_id__in=menu_ids))
        if role:
            serializer = SysRoleSerializer(role, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
            'code': 500,
            'msg': '角色不存在'
            }
        return JsonResponse(res)

    @has_permi('system:role:remove')
    def destroy(self, request, pk):
        """删除角色"""
        # pk = 1,2,3
        pks = pk.split(',')
        roles = SysRole.objects.filter(role_id__in=pks)
        if roles:
            roles.delete()
            res = {
                'code': 200,
                'msg': '角色删除成功'
            }
        else:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
        return JsonResponse(res)

    @has_permi('system:role:edit')
    def change_status(self, request):
        """修改角色状态"""
        role_id = request.data.get('role_id')
        status = request.data.get('status')
        role = SysRole.objects.filter(role_id=role_id).first()
        if role:
            role.status = status
            role.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
        return JsonResponse(res)

    def allocated_list(self, request):
        """已分配用户"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        role_id = request.query_params.get('role_id')
        username = request.query_params.get('username')
        phone_number = request.query_params.get('phone_number')

        query_condition = {}
        if username:
            query_condition['username__contains'] = username

        if phone_number:
            query_condition['phone_number__contains'] = phone_number

        role = SysRole.objects.filter(role_id=role_id).first()
        if role:
            users = role.sysuser_set.filter(**query_condition).order_by('create_time')
            paginator = Paginator(users, page_size)
            users = paginator.get_page(page_num)
            serializer = SysUserSerializer(users, many=True)
            res = {
                'code': 200,
                'msg': 'ok',
                'rows': serializer.data,
                'total': paginator.count
            }
        else:
            res = {
                'code': 200,
                'msg': 'ok'
            }
        return JsonResponse(res)

    def unallocated_list(self, request):
        """未分配用户"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        role_id = request.query_params.get('role_id')
        username = request.query_params.get('username')
        phone_number = request.query_params.get('phone_number')

        query_condition = {}
        if username:
            query_condition['username__contains'] = username

        if phone_number:
            query_condition['phone_number__contains'] = phone_number

        users = SysUser.objects.filter(Q(**query_condition) & ~Q(sysuserrole__role_id=role_id))

        paginator = Paginator(users, page_size)
        users = paginator.get_page(page_num)
        serializer = SysUserSerializer(users, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'rows': serializer.data,
            'total': paginator.count
        }
        return JsonResponse(res)

    def cancel(self, request):
        """取消用户角色"""
        res = {
            'code': 200,
            'msg': 'ok'
        }
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')
        user = SysUser.objects.filter(user_id=user_id).first()
        role = SysRole.objects.filter(role_id=role_id).first()
        if not role:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
            return JsonResponse(res)

        if not user:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
            return JsonResponse(res)

        user_role = SysUserRole.objects.filter(user=user,role=role).first()
        user_role.delete()

        return JsonResponse(res)

    def cancel_all(self, request):
        """批量取消授权角色"""
        role_id = request.query_params.get('role_id')
        user_ids = request.query_params.get('user_ids')
        user_ids = user_ids.split(',')
        role = SysRole.objects.filter(role_id=role_id).first()
        users = SysUser.objects.filter(user_id__in=user_ids)
        if not role:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
            return JsonResponse(res)

        if not users:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
            return JsonResponse(res)

        user_role = SysUserRole.objects.filter(role=role, user__in=users)
        user_role.delete()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    def select_all(self, request):
        """授权角色"""
        role_id = request.query_params.get('role_id')
        user_ids = request.query_params.get('user_ids')
        user_ids = user_ids.split(',')

        role = SysRole.objects.filter(role_id=role_id).first()
        users = SysUser.objects.filter(user_id__in=user_ids)
        if not role:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
            return JsonResponse(res)

        if not users:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
            return JsonResponse(res)

        role.sysuser_set.add(*users)
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    def data_scope(self, request):
        """数据权限"""
        role_id = request.data.get('role_id')
        dept_ids = request.data.get('dept_ids')
        data_scope = request.data.get('data_scope')
        role = SysRole.objects.filter(role_id=role_id).first()
        # 自定义数据权限
        if data_scope == '2':
            role.data_scope = data_scope
            depts = SysDept.objects.filter(dept_id__in=dept_ids)
            if role:
                role.save()
                role.depts.set(depts)
                res = {
                    'code': 200,
                    'msg': 'ok'
                }
            else:
                res = {
                    'code': 500,
                    'msg': '角色不存在'
                }
        # 全部数据权限/本部门数据权限/本部门及以下数据权限/仅本人数据权限
        else:
            role.data_scope = data_scope
            role.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        return JsonResponse(res)

    @has_permi('system:role:export')
    def export_xlsx(self, request):
        """导出角色数据"""
        page_num = request.data.get('page_num', 1)
        page_size = request.data.get('page_size', 10)
        role_name = request.data.get('role_name')
        role_key = request.data.get('role_key')
        status = request.data.get('status')
        begin_time = request.data.get('params[beginTime]')
        end_time = request.data.get('params[endTime]')

        query_condition = {}
        if role_name:
            query_condition['role_name'] = role_name

        if role_key:
            query_condition['role_key'] = role_key

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        roles = SysRole.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(roles, page_size)
        roles = paginator.get_page(page_num)

        header = ['角色ID', '角色名称', '角色权限字符', '状态', '创建时间']
        rows = [header]
        for role in roles:
            rows.append([role.role_id, role.role_name, role.role_key, role.status, role.create_time])

        return export_table('角色表.xlsx', rows)
