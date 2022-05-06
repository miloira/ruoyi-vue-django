from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from core.serializers import SysUserProfileSerializer, SysUserPasswordSerializer
from core.utils import get_perms


class UserProfileView(APIView):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """个人中心"""
        user = request.user
        permissions = get_perms(user)
        roles = [role.role_name for role in user.roles.all()]
        user_dict = SysUserProfileSerializer(user).data
        role_group = ",".join(roles)
        post_group = ",".join([post.post_name for post in user.posts.all()])

        res = {
            'code': 200,
            'msg': 'ok',
            'permissions': permissions,
            'roles': roles,
            'user': user_dict,
            'role_group': role_group,
            'post_group': post_group
        }
        return JsonResponse(res)

    def put(self, request):
        """基本资料"""
        serializer = SysUserProfileSerializer(request.user, request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            serializer = SysUserProfileSerializer(user)
            res = {
                'code': 200,
                'msg': 'ok',
                'user': serializer.data
            }
            return JsonResponse(res)


class UserProfilePasswordView(APIView):

    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """修改密码"""
        serializer = SysUserPasswordSerializer(request.user, request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            res = {
                'code': 200,
                'msg': 'ok'
            }
            return JsonResponse(res)