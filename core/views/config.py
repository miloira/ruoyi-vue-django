from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysConfig
from core.serializers import SysConfigSerializer
from core.utils import export_table

@monitor
class ConfigView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @has_permi('system:config:list')
    def list(self, request):
        """参数设置列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        config_name = request.query_params.get('config_name')
        config_key = request.query_params.get('config_key')
        config_type = request.query_params.get('config_type')
        begin_time = request.query_params.get('params[beginTime]')
        end_time = request.query_params.get('params[endTime]')

        query_condition = {}
        if config_name:
            query_condition['config_name__contains'] = config_name

        if config_key:
            query_condition['config_key__contains'] = config_key

        if config_type:
            query_condition['config_type'] = config_type

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        configs = SysConfig.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(configs, page_size)
        configs = paginator.get_page(page_num)
        serializer = SysConfigSerializer(configs, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'total': paginator.count,
            'rows': serializer.data
        }
        return JsonResponse(res)

    @has_permi('system:config:add')
    def create(self, request):
        """新增参数设置"""
        request.data['create_by'] = request.user.username
        serializer = SysConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:config:edit')
    def update(self, request):
        """更新参数设置"""
        request.data['update_by'] = request.user.username
        config_id = request.data.get('config_id')
        config = SysConfig.objects.filter(config_id=config_id).first()
        if config:
            serializer = SysConfigSerializer(config, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '参数设置不存在'
            }
        return JsonResponse(res)

    @has_permi('system:config:query')
    def retrieve(self, request, pk):
        """参数设置详情"""
        config = SysConfig.objects.filter(config_id=pk).first()
        if config:
            serializer = SysConfigSerializer(config)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '参数设置不存在'
            }
        return JsonResponse(res)

    @has_permi('system:config:remove')
    def destroy(self, request, pk):
        """删除参数设置"""
        # pk = 1,2,3
        pks = pk.split(',')
        configs = SysConfig.objects.filter(config_id__in=pks)
        if configs:
            configs.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '参数设置不存在'
            }
        return JsonResponse(res)

    def get_value(self, request, key):
        """获取参数设置键值"""
        config = SysConfig.objects.filter(config_key=key).first()
        if config:
            res = {
                'code': 200,
                'msg': config.config_value
            }
        else:
            res = {
                'code': 500,
                'msg': '参数设置不存在'
            }
        return JsonResponse(res)

    def refresh_cache(self, request):
        """刷新缓存"""
        return JsonResponse({})

    @has_permi('system:config:export')
    def export_xlsx(self, request):
        """导出参数设置数据"""
        page_num = request.data.get('page_num', 1)
        page_size = request.data.get('page_size', 10)
        config_name = request.data.get('config_name')
        config_key = request.data.get('config_key')
        config_type = request.data.get('config_type')
        begin_time = request.data.get('params[beginTime]')
        end_time = request.data.get('params[endTime]')

        query_condition = {}
        if config_name:
            query_condition['config_name__contains'] = config_name

        if config_key:
            query_condition['config_key__contains'] = config_key

        if config_type:
            query_condition['config_type'] = config_type

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        configs = SysConfig.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(configs, page_size)
        configs = paginator.get_page(page_num)
        header = ['参数主键', '参数名称', '参数键名', '参数键值', '系统内置', '备注', '创建时间']
        rows = [header]
        for config in configs:
            rows.append([config.config_id, config.config_name, config.config_key, config.config_value, config.config_type, config.remark, config.create_time])

        return export_table('参数设置表.xlsx', rows)
