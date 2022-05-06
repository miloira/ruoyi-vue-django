from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysPost
from core.serializers import SysPostSerializer
from core.utils import export_table

@monitor
class PostView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:post:list')
    def list(self, request):
        """岗位列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        post_code = request.query_params.get('post_code')
        post_name = request.query_params.get('post_name')
        status = request.query_params.get('status')

        query_condition = {}
        if post_code:
            query_condition['post_code__icontains'] = post_code
        if post_name:
            query_condition['post_name__icontains'] = post_name
        if status:
            query_condition['status'] = status

        posts = SysPost.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(posts, page_size)
        posts = paginator.get_page(page_num)
        serializer = SysPostSerializer(posts, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'rows': serializer.data,
            'total': paginator.count
        }
        return JsonResponse(res)

    @has_permi('system:post:add')
    def create(self, request):
        """新增岗位"""
        request.data['create_by'] = request.user.username
        serializer = SysPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:post:edit')
    def update(self, request):
        """修改岗位"""
        request.data['update_by'] = request.user.username
        post_id = request.data.get('post_id')
        post = SysPost.objects.filter(post_id=post_id).first()
        if post:
            serializer = SysPostSerializer(post, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '岗位不存在'
            }
        return JsonResponse(res)

    @has_permi('system:post:query')
    def retrieve(self, request, pk):
        """岗位详情"""
        post = SysPost.objects.filter(post_id=pk).first()
        serializer = SysPostSerializer(post)
        if post:
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '岗位不存在'
            }
        return JsonResponse(res)

    @has_permi('system:post:remove')
    def destroy(self, request, pk):
        """删除岗位"""
        # pk = 1,2,3
        pks = pk.split(',')
        posts = SysPost.objects.filter(post_id__in=pks)
        if posts:
            posts.delete()
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

    @has_permi('system:post:export')
    def export_xlsx(self, request):
        """导出岗位数据"""
        page_num = request.data.get('page_num', 1)
        page_size = request.data.get('page_size', 10)
        post_code = request.data.get('post_code')
        post_name = request.data.get('post_name')
        status = request.data.get('status')

        query_condition = {}
        if post_code:
            query_condition['post_code__icontains'] = post_code

        if post_name:
            query_condition['post_name__icontains'] = post_name

        if status:
            query_condition['status'] = status

        posts = SysPost.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(posts, page_size)
        posts = paginator.get_page(page_num)
        header = ['岗位编号', '岗位编码', '岗位名称', '岗位排序', '状态', '创建时间']
        rows = [header]
        for post in posts:
            rows.append([post.post_id, post.post_code, post.post_name, post.post_sort, post.status, post.create_time])

        return export_table('岗位表.xlsx', rows)
