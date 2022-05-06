from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysLoginLog
from core.serializers import SysLoginLogSerializer
from core.utils import export_table

@monitor
class LoginLogView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('monitor:logininfor:list')
    def list(self, request):
        """登录日志列表"""
        page_num = request.query_params.get('page_num')
        page_size = request.query_params.get('page_size')
        ip_addr = request.query_params.get('ip_addr')
        username = request.query_params.get('username')
        status = request.query_params.get('status')
        begin_time = request.query_params.get('params[beginTime]')
        end_time = request.query_params.get('params[endTime]')

        query_condition = {}
        if ip_addr:
            query_condition['ip_addr__contains'] = ip_addr

        if username:
            query_condition['username__contains'] = username

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        login_logs = SysLoginLog.objects.filter(**query_condition).order_by('-create_time')
        paginator = Paginator(login_logs, page_size)
        login_logs = paginator.get_page(page_num)
        serializer = SysLoginLogSerializer(login_logs, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'total': paginator.count,
            'rows': serializer.data
        }
        return JsonResponse(res)

    @has_permi('monitor:logininfor:remove')
    def destroy(self, request, pk):
        """删除登录日志"""
        # pk = 1,2,3
        pks = pk.split(',')
        login_logs = SysLoginLog.objects.filter(info_id__in=pks)
        if login_logs:
            login_logs.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '操作日志不存在'
            }
        return JsonResponse(res)

    @has_permi('monitor:logininfor:remove')
    def clean_all(self, request):
        """清空登录日志"""
        SysLoginLog.objects.all().delete()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('monitor:logininfor:export')
    def export_xlsx(self, request):
        """导出登录日志数据"""
        page_num = request.data.get('page_num')
        page_size = request.data.get('page_size')
        ip_addr = request.data.get('ip_addr')
        username = request.data.get('username')
        status = request.data.get('status')
        begin_time = request.data.get('params[beginTime]')
        end_time = request.data.get('params[endTime]')

        query_condition = {}
        if ip_addr:
            query_condition['ip_addr__contains'] = ip_addr

        if username:
            query_condition['username__contains'] = username

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        login_logs = SysLoginLog.objects.filter(**query_condition).order_by('-create_time')
        paginator = Paginator(login_logs, page_size)
        login_logs = paginator.get_page(page_num)
        header = ['访问编号', '用户名称', '登录地址', '登录地点', '浏览器', '操作系统', '登录状态', '操作信息', '登录日期']
        rows = [header]
        for login_log in login_logs:
            rows.append([login_log.info_id, login_log.username, login_log.ip_addr, login_log.login_location, login_log.browser, login_log.os, login_log.status, login_log.msg, login_log.login_time])

        return export_table('登录日志表.xslx', rows)
