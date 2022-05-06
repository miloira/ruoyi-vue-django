import datetime
import getpass
import platform

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
import psutil
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.decorator import has_permi


class ServerView(GenericViewSet):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @has_permi('monitor:server:list')
    def list(self, request):
        """服务监控"""
        psutil.cpu_count()
        cpu_used = psutil.cpu_percent()
        cpu_free = 100 - cpu_used

        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        run_time = datetime.datetime.now() - boot_time
        day = int(run_time.total_seconds() / (3600 * 24))
        hour = int((run_time.total_seconds() - day * 3600 * 24) / 3600)
        minute = int((run_time.total_seconds() - day * 3600 * 24 - hour * 3600) / 60)
        second = int(run_time.total_seconds() - day * 3600 * 24 - hour * 3600 - minute * 60)

        disks = []
        for p in psutil.disk_partitions():
            disk = psutil.disk_usage(p.mountpoint)
            disks.append({
                'dir_name': p.mountpoint,
                'free': f'{round(disk.free / 2 ** 30, 2)} GB',
                'sys_type_name': p.fstype,
                'total': f'{round(disk.total / 2 ** 30, 2)} GB',
                'type_name': p.device,
                'used': f'{round(disk.used / 2 ** 30, 2)} GB',
                'usage': round(disk.percent, 2),
            })

        res = {
            'code': 200,
            'msg': 'ok',
            'data': {
                'cpu': {
                    'cpu_count_physical': psutil._psplatform.cpu_count_physical(),
                    'cpu_count_logical': psutil._psplatform.cpu_count_logical(),
                    'free': cpu_free,
                    'used': cpu_used
                },
                'mem': {
                    'free': round(psutil.virtual_memory().free / 2 ** 30, 2),
                    'total': round(psutil.virtual_memory().total / 2 ** 30, 2),
                    'used': round(psutil.virtual_memory().used / 2 ** 30, 2),
                    'usage': psutil.virtual_memory().percent
                },
                'sys': {
                    'user': getpass.getuser(),
                    'computer_name': platform.node(),
                    'os_arch': platform.machine(),
                    'os_name': platform.system() + platform.release(),
                    'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'run_time': f'{day} 天 {hour} 时 {minute} 分 {second} 秒'
                },
                'disk': disks
            }
        }
        return JsonResponse(res)
