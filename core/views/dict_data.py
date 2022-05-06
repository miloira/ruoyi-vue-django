from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import monitor, has_permi
from core.models import SysDictData, SysDictType
from core.serializers import SysDictDataSerializer, SysDictTypeSerializer
from core.utils import export_table

@monitor
class DictDataView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:dict:list')
    def list(self, request):
        """字典数据列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        dict_type = request.query_params.get('dict_type')
        dict_label = request.query_params.get('dict_label')
        status = request.query_params.get('status')

        query_condition = {}
        if dict_label:
            query_condition['dict_label__contains'] = dict_label

        if dict_type:
            query_condition['dict_type__dict_type__contains'] = dict_type

        if status:
            query_condition['status'] = status

        dict_type = SysDictType.objects.filter(dict_type=dict_type).first()
        dict_data = dict_type.sysdictdata_set.filter(**query_condition).order_by('create_time')
        paginator = Paginator(dict_data, page_size)
        dict_data = paginator.get_page(page_num)
        serializer = SysDictDataSerializer(dict_data, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'rows': serializer.data,
            'total': paginator.count
        }
        return JsonResponse(res)

    @has_permi('system:dict:add')
    def create(self, request):
        """新增字典数据"""
        request.data['create_by'] = request.user.username
        dict_type = SysDictType.objects.filter(dict_type=request.data.get('dict_type')).first()
        if dict_type:
            request.data['dict_type'] = dict_type.dict_id
            serializer = SysDictDataSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '字典类型不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dict:edit')
    def update(self, request):
        """修改字典数据"""
        request.data['update_by'] = request.user.username
        dict_code = request.data.get('dict_code')
        dict_data = SysDictData.objects.filter(dict_code=dict_code).first()
        if dict_data:
            serializer = SysDictDataSerializer(dict_data, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '字典数据不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dict:query')
    def retrieve(self, request, pk):
        """字典数据详情"""
        dict_data = SysDictData.objects.filter(dict_code=pk).first()
        if dict_data:
            serializer = SysDictDataSerializer(dict_data)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '字典类型不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dict:remove')
    def destroy(self, request, pk):
        """删除字典数据"""
        # pk = 1,2,3
        pks = pk.split(',')
        dict_data = SysDictData.objects.filter(dict_code__in=pks)
        if dict_data:
            dict_data.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '字典数据不存在'
            }
        return JsonResponse(res)

    def dict_data(self, request, value):
        """正常/停用"""
        dict_type = SysDictType.objects.filter(dict_type=value).first()
        if dict_type:
            dict_data = dict_type.sysdictdata_set.all()
            serializer = SysDictDataSerializer(dict_data, many=True)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '字典类型不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dict:export')
    def export_xlsx(self, request):
        """导出字典数据数据"""
        page_num = request.data.get('page_num', 1)
        page_size = request.data.get('page_size', 10)
        dict_type = request.data.get('dict_type')
        dict_label = request.data.get('dict_label')
        status = request.data.get('status')

        query_condition = {}
        if dict_label:
            query_condition['dict_label__contains'] = dict_label

        if dict_type:
            query_condition['dict_type__dict_type__contains'] = dict_type

        if status:
            query_condition['status'] = status

        dict_type = SysDictType.objects.filter(dict_type=dict_type).first()
        dict_data = dict_type.sysdictdata_set.filter(**query_condition).order_by('create_time')
        paginator = Paginator(dict_data, page_size)
        dict_data = paginator.get_page(page_num)
        header = ['字典编码', '字典标签', '字典键值', '字典排序', '状态', '备注', '创建时间']
        rows = [header]
        for obj in dict_data:
            rows.append([obj.dict_code, obj.dict_label, obj.dict_value, obj.dict_sort, obj.status, obj.remark, obj.create_time])

        return export_table('字典数据表.xlsx', rows)

@monitor
class DictTypeView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('system:dict:list')
    def list(self, request):
        """字典类型列表"""
        page_num = request.query_params.get('page_num', 1)
        page_size = request.query_params.get('page_size', 10)
        dict_name = request.query_params.get('dict_name')
        dict_type = request.query_params.get('dict_type')
        status = request.query_params.get('status')
        begin_time = request.query_params.get('params[beginTime]')
        end_time = request.query_params.get('params[endTime]')

        query_condition = {}
        if dict_name:
            query_condition['dict_name__contains'] = dict_name

        if dict_type:
            query_condition['dict_type__contains'] = dict_type

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        dict_types = SysDictType.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(dict_types, page_size)
        dict_types = paginator.get_page(page_num)
        serializer = SysDictTypeSerializer(dict_types, many=True)
        res = {
            'code': 200,
            'msg': 'ok',
            'rows': serializer.data,
            'total': paginator.count
        }
        return JsonResponse(res)

    @has_permi('system:dict:add')
    def create(self, request):
        """新增字典类型"""
        request.data['create_by'] = request.user.username
        serializer = SysDictTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:dict:edit')
    def update(self, request):
        """修改字典类型"""
        request.data['update_by'] = request.user.username
        dict_id = request.data.get('dict_id')
        dict_type = SysDictType.objects.filter(dict_id=dict_id).first()
        serializer = SysDictTypeSerializer(dict_type, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

    @has_permi('system:dict:query')
    def retrieve(self, request, pk):
        """字典类型详情"""
        dict_type = SysDictType.objects.filter(dict_id=pk).first()
        if dict_type:
            serializer = SysDictTypeSerializer(dict_type)
            res = {
                'code': 200,
                'msg': 'ok',
                'data': serializer.data
            }
        else:
            res = {
                'code': 500,
                'msg': '字典类型不存在'
            }
        return JsonResponse(res)

    @has_permi('system:dict:remove')
    def destroy(self, request, pk):
        """删除字典类型"""
        dict_type = SysDictType.objects.filter(dict_id=pk).first()
        if dict_type:
            dict_type.delete()
            res = {
                'code': 200,
                'msg': 'ok'
            }
        else:
            res = {
                'code': 500,
                'msg': '字典类型不存在'
            }
        return JsonResponse(res)

    def refresh_cache(self, request):
        """刷新缓存"""
        return JsonResponse({})

    def option_select(self, request):
        """选项"""
        return JsonResponse({})

    @has_permi('system:dict:export')
    def export_xlsx(self, request):
        """字典类型数据导出"""
        page_num = request.data.get('page_num', 1)
        page_size = request.data.get('page_size', 10)
        dict_name = request.data.get('dict_name')
        dict_type = request.data.get('dict_type')
        status = request.data.get('status')
        begin_time = request.data.get('params[beginTime]')
        end_time = request.data.get('params[endTime]')

        query_condition = {}
        if dict_name:
            query_condition['dict_name__contains'] = dict_name

        if dict_type:
            query_condition['dict_type__contains'] = dict_type

        if status:
            query_condition['status'] = status

        if begin_time and end_time:
            query_condition['create_time__range'] = [begin_time, end_time]

        dict_types = SysDictType.objects.filter(**query_condition).order_by('create_time')
        paginator = Paginator(dict_types, page_size)
        dict_types = paginator.get_page(page_num)
        header = ['字典编号', '字典名称', '字典类型', '状态', '备注', '创建时间']
        rows = [header]
        for dict_type in dict_types:
            rows.append([dict_type.dict_id, dict_type.dict_name, dict_type.dict_type, dict_type.status, dict_type.remark, dict_type.create_time])

        return export_table('字典类型表.xlsx', rows)
