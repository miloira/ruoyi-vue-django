from datetime import datetime

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_response_payload_handler
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from gvcode import VFCode

from core.models import SysMenu, SysRoleMenu, SysUserRole
from core.serializers import LoginSerializer, SysMenuSerializer, SysUserProfileSerializer
from core.utils import is_admin, gen_routers, get_perms


class CaptchaView(APIView):

    def get(self, request):
        """获取验证码"""
        vf = VFCode()
        vf.generate_digit(4)
        cache.set(vf.code, vf.code, 3 * 60)
        data = {
            'code': 200,
            'msg': 'ok',
            'data': {
                'captcha': vf.get_img_base64()[1],
                'code': vf.code
            }
        }
        return JsonResponse(data)

class LoginView(JSONWebTokenAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        error_msg = list(serializer.errors.values())[0][0]

        # 验证码错误
        if error_msg == '验证码错误':
            res = {
                'code': 10001,
                'msg': error_msg
            }
        elif error_msg == '需同时提供用户名和密码':
            res = {
                'code': 10002,
                'msg': error_msg
            }
        # 用户名或密码错误
        elif error_msg == '用户名或密码错误':
            res = {
                'code': 10003,
                'msg': error_msg
            }
        elif error_msg == '账号已停用':
            res = {
                'code': 10004,
                'msg': error_msg
            }
        # JWT相关错误
        else:
            res = {
                'code': 401,
                'msg': list(serializer.errors.values())[0][0]
            }
        return Response(res)

class UserInfoView(APIView):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """个人信息"""
        user = request.user
        permissions = get_perms(user)
        roles = [role.role_name for role in user.roles.all()]
        user = SysUserProfileSerializer(user).data
        res = {
            'code': 200,
            'msg': 'ok',
            'permissions': permissions,
            'roles': roles,
            'user': user
        }
        return JsonResponse(res)

class RoutersView(APIView):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """路由信息"""
        sys_user = request.user
        if is_admin(sys_user):
            menus = SysMenu.objects.all().order_by('order_num')
            sys_menu_list = [SysMenuSerializer(obj).data for obj in menus]
        else:
            roles = SysUserRole.objects.filter(user=sys_user, role__status='0')
            role_menu = SysRoleMenu.objects.filter(role_id__in=[obj.role_id for obj in roles])

            menus = SysMenu.objects.filter(
                menu_type__in=['M', 'C'],
                menu_id__in=[obj.menu_id for obj in role_menu],
                is_delete=False,
                visible='0'
            ).order_by('order_num')
            sys_menu_list = [SysMenuSerializer(obj).data for obj in menus]

        sys_menu_list_top = []
        for item in sys_menu_list:
            if item.get("parent_id") == 0:
                sys_menu_list_top.append(item)
        data = gen_routers(sys_menu_list_top, sys_menu_list)

        res = {
            "code": 200,
            "msg": "ok",
            "data": data or []
        }
        return JsonResponse(data=res)

class LogoutView(APIView):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """注销"""
        res = {
            'code': 200,
            'msg': 'ok'
        }
        return JsonResponse(res)

