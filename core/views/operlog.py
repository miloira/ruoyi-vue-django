from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import has_permi
from core.models import SysOperationLog
from core.serializers import SysOperationLogSerializer
from core.utils import export_table



class OperationLogView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('monitor:operlog:list')
    def list(self, request):
        """操作日志列表"""
        page_num = request.query_params.get('page_num')
        page_size = request.query_params.get('page_size')
        title = request.query_params.get('title')
        operator = request.query_params.get('operator')
        business_type = request.query_params.get('business_type')
        status = request.query_params.get('status')
        begin_time = request.query_params.get('params[beginTime]')
        end_time = request.query_params.get('params[endTime]')

        query_condition = {}
        if title:
            query_condition['title__contains'] = title

        if operator:
            query_condition['operator__contains'] = operator

        if business_type:
            query_condition['business_type'] = business_type

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        operation_logs = SysOperationLog.objects.filter(**query_condition).order_by('-create_time')
        paginator = Paginator(operation_logs, page_size)
        operation_logs = paginator.get_page(page_num)
        serializer = SysOperationLogSerializer(operation_logs, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'total': paginator.count,
            'rows': serializer.data
        }
        return JsonResponse(res)

    @has_permi('monitor:operlog:remove')
    def destroy(self, request, pk):
        """删除操作日志"""
        # pk = 1,2,3
        pks = pk.split(',')
        operation_logs = SysOperationLog.objects.filter(id__in=pks)
        if operation_logs:
            operation_logs.delete()
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

    @has_permi('monitor:operlog:remove')
    def clean_all(self, request):
        """清空操作日志"""
        SysOperationLog.objects.all().delete()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('monitor:operlog:export')
    def export_xlsx(self, request):
        """导出操作日志数据"""
        page_num = request.data.get('page_num')
        page_size = request.data.get('page_size')
        title = request.data.get('title')
        operator = request.data.get('operator')
        business_type = request.data.get('business_type')
        status = request.data.get('status')
        begin_time = request.data.get('params[beginTime]')
        end_time = request.data.get('params[endTime]')

        query_condition = {}
        if title:
            query_condition['title__contains'] = title

        if operator:
            query_condition['operator__contains'] = operator

        if business_type:
            query_condition['business_type'] = business_type

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        operation_logs = SysOperationLog.objects.filter(**query_condition).order_by('-create_time')
        paginator = Paginator(operation_logs, page_size)
        operation_logs = paginator.get_page(page_num)
        header = ['日志编号', '系统模块', '操作类型', '请求方式', '操作人员', '操作地址', '操作地点', '操作日期']
        rows = [header]
        for operation_log in operation_logs:
            rows.append([operation_log.id, operation_log.title, operation_log.business_type, operation_log.request_method, operation_log.operator, operation_log.ip, operation_log.location, operation_log.create_time])

        return export_table('操作日志.xlsx', rows)
