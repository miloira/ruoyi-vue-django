from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysNotice
from core.serializers import SysNoticeSerializer

@monitor
class NoticeView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:notice:list')
    def list(self, request):
        """通知公告列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        notice_title = request.query_params.get('notice_title')
        notice_type = request.query_params.get('notice_type')
        create_by = request.query_params.get('create_by')

        query_condition = {}
        if notice_title:
            query_condition['notice_title__contains'] = notice_title

        if notice_type:
            query_condition['notice_type'] = notice_type

        if create_by:
            query_condition['create_by__contains'] = create_by

        notices = SysNotice.objects.filter(**query_condition).order_by('-create_time')
        paginator = Paginator(notices, page_size)
        notices = paginator.get_page(page_num)
        serializer = SysNoticeSerializer(notices, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'total': paginator.count,
            'rows': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:notice:add')
    def create(self, request):
        """新增通知公告"""
        request.data['create_by'] = request.user.username
        serializer = SysNoticeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:notice:edit')
    def update(self, request):
        """修改通知公告"""
        request.data['update_by'] = request.user.username
        notice = SysNotice.objects.filter(notice_id=request.data.get('notice_id')).first()
        if notice:
            serializer = SysNoticeSerializer(notice, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '通知公告不存在'
            }
        return JsonResponse(res)

    @has_permi('system:notice:query')
    def retrieve(self, request, pk):
        """通知公告详情"""
        notice = SysNotice.objects.filter(notice_id=pk).first()
        if notice:
            serializer = SysNoticeSerializer(notice)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '通知公告不存在'
            }
        return JsonResponse(res)

    @has_permi('system:notice:remove')
    def destroy(self, request, pk):
        """删除通知公告"""
        # pk = 1,2,3
        pks = pk.split(',')
        notices = SysNotice.objects.filter(notice_id__in=pks)
        if notices:
            notices.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '通知公告不存在'
            }
        return JsonResponse(res)
