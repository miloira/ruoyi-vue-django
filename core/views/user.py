import re

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from openpyxl import load_workbook

from core.serializers import SysUserSerializer, SysUserProfileSerializer, SysRoleSerializer, SysPostSerializer
from core.models import SysUser, SysPost, SysDept, SysRole
from core.utils import export_table
from core.decorator import monitor, has_permi

@monitor
class UserView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:user:list')
    def list(self, request):
        """用户列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        dept_id = request.query_params.get('dept')
        userName = request.query_params.get('username')
        phone_number = request.query_params.get('phone_number')
        status = request.query_params.get('status')
        beginTime = request.query_params.get('params[beginTime]')
        endTime = request.query_params.get('params[endTime]')

        query_condition = {}
        if dept_id:
            query_condition['dept__dept_id'] = dept_id

        if userName:
            query_condition['username__contains'] = userName

        if phone_number:
            query_condition['phone_number__contains'] = phone_number

        if status:
            query_condition['status'] = status

        if beginTime and endTime:
            query_condition['create_time__range'] = [beginTime, endTime]

        users = SysUser.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(users, page_size)
        users = paginator.get_page(page_num)
        serializer = SysUserProfileSerializer(users, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'rows': serializer.data,
            'total': paginator.count
        }
        return JsonResponse(res)

    @has_permi('system:user:query')
    def retrieve(self, request, pk):
        """用户详情"""
        try:
            user = SysUser.objects.get(pk=pk)
        except SysUser.DoesNotExist:
            res = {
                'code': 500,
                'msg': '用户不存在',
            }
            return JsonResponse(res)

        serializer = SysUserSerializer(user)
        posts = SysPostSerializer(SysPost.objects.all(), many=True).data
        roles = SysRoleSerializer(SysRole.objects.all(), many=True).data
        res = {
            'code': 200,
            'msg': 'ok',
            'data': serializer.data,
            'posts': posts,
            'roles': roles,
            'post_ids': [post.post_id for post in user.posts.all()],
            'role_ids': [role.role_id for role in user.roles.all()],
        }
        return JsonResponse(res)

    @has_permi('system:user:add')
    def create(self, request):
        """新增用户"""
        request.data['create_by'] = request.user.username
        username = request.data.get('username')
        nickname = request.data.get('nickname')
        password = request.data.get('password')
        sex = request.data.get('sex')
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        status = request.data.get('status')
        remark = request.data.get('remark')
        dept = request.data.get('dept')
        posts = request.data.get('posts')
        roles = request.data.get('roles')

        condition = {}
        if username:
            condition['username'] = username

        if nickname:
            condition['nickname'] = nickname

        if sex:
            condition['sex'] = sex

        if email:
            condition['email'] = email

        if remark:
            condition['remark'] = remark

        if phone_number:
            condition['phone_number'] = phone_number

        if status:
            condition['status'] = status

        if dept:
            condition['dept'] = SysDept.objects.get(dept_id=dept)

        with transaction.atomic():
            user = SysUser(**condition)
            user.set_password(password)
            user.save()
            user.roles.set([SysRole.objects.get(role_id=role_id) for role_id in roles])
            user.posts.set([SysPost.objects.get(post_id=post_id) for post_id in posts])

        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:user:edit')
    def update(self, request):
        """修改用户"""
        request.data['update_by'] = request.user.username
        user = SysUser.objects.filter(pk=request.data['user_id']).first()
        if not user:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
            return JsonResponse(res)
        serializer = SysUserSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            role_ids = request.data['roles']
            post_ids = request.data['posts']
            user.dept = SysDept.objects.filter(dept_id=request.data.get('dept')).first() or SysDept.objects.filter(
                dept_id=1).first()
            user.save()
            user.roles.set([SysRole.objects.get(role_id=role_id) for role_id in role_ids])
            user.posts.set([SysPost.objects.get(post_id=post_id) for post_id in post_ids])
            res = {
                'code': 200,
                'msg': 'ok'
            }
            return JsonResponse(res)

    @has_permi('system:user:remove')
    def destroy(self, request, pk):
        """删除用户"""
        # pk = 1,2,3
        pks = pk.split(',')
        users = SysUser.objects.filter(user_id__in=pks)
        if users:
            users.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
        return JsonResponse(res)

    def option(self, request):
        """岗位和角色选项"""
        posts = SysPost.objects.all()
        roles = SysRole.objects.all()
        posts = SysPostSerializer(posts, many=True).data
        roles = SysRoleSerializer(roles, many=True).data
        res = {
            'code': 200,
            'msg': 'ok',
            'posts': posts,
            'roles': roles,
        }
        return JsonResponse(res)

    @has_permi('system:user:edit')
    def change_status(self, request):
        """修改用户状态"""
        user_id = request.data.get('user_id')
        status = request.data.get('status')
        user = SysUser.objects.filter(user_id=user_id).first()

        if user:
            user.status = status
            user.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
        return JsonResponse(res)

    @has_permi('system:user:export')
    def export_xlsx(self, request):
        """导出用户数据"""
        pageNum = request.data.get('page_num', 1)
        pageSize = request.data.get('page_size', 10)
        deptId = request.data.get('dept')
        userName = request.data.get('username')
        phone_number = request.data.get('phone_number')
        status = request.data.get('status')
        begin_time = request.data.get('params[beginTime]')
        end_time = request.data.get('params[endTime]')

        query_condition = {}
        if deptId:
            query_condition['dept__dept_id'] = deptId

        if userName:
            query_condition['username__contains'] = userName

        if phone_number:
            query_condition['phone_number__contains'] = phone_number

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        users = SysUser.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(users, pageSize)
        users = paginator.get_page(pageNum)

        header = ['用户ID', '用户名称', '用户昵称', '手机号', '用户邮箱', '状态', '部门名称', '部门负责人', '上次登录时间', '账号创建时间']
        rows = [header]
        for user in users:
            rows.append([user.user_id, user.username, user.nickname, user.phone_number, user.email, user.status,
                         user.dept.dept_name, user.dept.leader, user.login_date, user.create_time])

        return export_table('用户表.xlsx', rows)

    @has_permi('system:user:import')
    def import_xlsx(self, request):
        """导入用户数据"""
        res = {
            'code': 200,
            'msg': 'ok'
        }
        update_support = request.query_params.get('update_support') or 'false'
        file = request.data['file']
        wb = load_workbook(file)
        ws = wb.active
        users = []
        try:
            if update_support == 'true':
                for row in list(ws.values)[1:]:
                    user_data = {
                        'user_id': row[0],
                        'username': row[1],
                        'nickname': row[2],
                        'phone_number': row[3],
                        'email': row[4],
                        'status': row[5],
                        'dept': SysDept.objects.filter(dept_name=row[6]).first(),
                        'login_date': row[8],
                        'create_time': row[9]
                    }
                    users.append(SysUser(**user_data))
                fields = ['username', 'nickname', 'phone_number', 'email', 'status', 'dept', 'login_date', 'create_time']
                SysUser.objects.bulk_update(users, fields)
            else:
                for row in list(ws.values)[1:]:
                    user_data = {
                        'username': row[1],
                        'nickname': row[2],
                        'phone_number': row[3],
                        'email': row[4],
                        'status': row[5],
                        'dept': SysDept.objects.filter(dept_name=row[6]).first(),
                        'login_date': row[8],
                        'create_time': row[9]
                    }
                    users.append(SysUser(**user_data))
                SysUser.objects.bulk_create(users)
        except Exception as e:
            # print(e)
            res['code'] = 500
            res['msg'] = '导入失败'

        return JsonResponse(res)

    def import_template(self, request):
        """导入模板"""
        return export_table('用户表.xlsx', [])

    @has_permi('system:user:resetPwd')
    def reset_pwd(self, request):
        """重置密码"""
        user = SysUser.objects.filter(user_id=request.data.get('user_id')).first()
        password = request.data.get('password')
        if user:
            res = {
                'code': 200,
                'msg': 'ok'
            }
            user.set_password(password)
            user.save()
        else:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
        return JsonResponse(res)

    def auth_role(self, request, pk):
        """可分配角色"""
        user = SysUser.objects.filter(user_id=pk).first()
        if user:
            res = {
                'code': 200,
                'msg': 'ok',
                'roles': SysRoleSerializer(SysRole.objects.exclude(sysuserrole__user=user), many=True).data,
                'user': SysUserSerializer(user).data
            }
        else:
            res = {
                'code': 500,
                'msg': '用户不存在'
            }
        return JsonResponse(res)

    def add_role(self, request, pk):
        """分配角色"""
        res = {
            'code': 200,
            'msg': 'ok'
        }
        user = SysUser.objects.filter(user_id=pk).first()
        if not user:
            res['msg'] = '用户不存在'
            return JsonResponse(res)

        role_ids = request.data.get('role_ids')
        if not role_ids:
            res['msg'] = '缺少role_ids参数'
            return JsonResponse(res)

        if not re.match('\d[,\d]*', role_ids):
            res['msg'] = 'role_ids参数格式错误'
            return JsonResponse(res)

        role_ids = role_ids.split(',')
        user.roles.add(*SysRole.objects.filter(role_id__in=role_ids))

        return JsonResponse(res)
