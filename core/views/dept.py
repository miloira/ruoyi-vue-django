from django.db.models import Q
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysDept, SysRole
from core.serializers import SysDeptSerializer
from core.utils import get_label_tree

@monitor
class DeptView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_ancestors(self, depts, dept_id):
        ancestors = [str(dept_id)]
        for d in depts:
            if d.dept_id == dept_id:
                dept_id = d.parent_id
                if dept_id == 0:
                    break
                ancestors.append(str(dept_id))
        return ','.join(reversed(ancestors))

    @has_permi('system:dept:list')
    def list(self, request):
        dept_name = request.query_params.get('dept_name')
        status = request.query_params.get('status')

        query_condition = {}
        if dept_name:
            query_condition['dept_name'] = dept_name

        if status:
            query_condition['status'] = status

        depts = SysDept.objects.filter(**query_condition)
        serializer = SysDeptSerializer(depts, many=True)
        for dept in serializer.data:
            dept['children'] = []

        res = {
            'code': 200,
            'msg': 'ok',
            'data': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:dept:query')
    def retrieve(self, request, pk):
        """部门详情"""
        dept = SysDept.objects.filter(dept_id=pk).first()
        if dept:
            serializer = SysDeptSerializer(dept)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '部门不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dept:add')
    def create(self, request):
        """新增部门"""
        request.data['create_by'] = request.user.username
        depts = SysDept.objects.all()
        request.data['ancestors'] = self.get_ancestors(depts, request.data.get('parent_id'))
        serializer = SysDeptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:dept:edit')
    def update(self, request):
        """修改部门"""
        request.data['update_by'] = request.user.username
        dept_id = request.data.get('dept_id')
        dept = SysDept.objects.filter(dept_id=dept_id).first()
        if dept:
            serializer = SysDeptSerializer(dept, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '部门不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dept:remove')
    def destroy(self, request, pk):
        """删除部门"""
        dept = SysDept.objects.filter(dept_id=pk).first()
        if dept:
            dept.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '部门不存在'
            }
        return JsonResponse(res)

    def exclude(self, request, pk):
        """排除结点的部门树"""
        dept = SysDept.objects.filter(dept_id=pk).first()
        if dept:
            depts = SysDept.objects.filter(~Q(dept_id=dept.dept_id))
            serializer = SysDeptSerializer(depts, many=True)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '部门不存在'
            }
        return JsonResponse(res)

    def tree_select(self, request):
        """部门树"""
        objects = SysDept.objects.all()
        res_objects_list = [{"id": item.dept_id, "label": item.dept_name, "parent_id": item.parent_id} for item in objects]
        tree = get_label_tree(res_objects_list)
        res = {
            'code': 200,
            'msg': 'ok',
            'data': tree or []
        }
        return JsonResponse(res)

    def role_dept_tree_select(self, request, pk):
        """角色部门树"""
        role = SysRole.objects.filter(role_id=pk).first()
        if role:
            checked_keys = [dept.dept_id for dept in role.depts.all()]
            objects = SysDept.objects.all()
            res_objects_list = [{"id": item.dept_id, "label": item.dept_name, "parent_id": item.parent_id} for item in
                                objects]
            tree = get_label_tree(res_objects_list)
            res = {
                'code': 200,
                'msg': 'ok',
                'depts': tree or [],
                'checked_keys': checked_keys
            }
        else:
            res = {
                'code': 500,
                'msg': '角色不存在'
            }
        return JsonResponse(res)
