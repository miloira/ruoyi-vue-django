from django.contrib.auth import authenticate
from django.core.cache import cache
from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from user_agents import parse

from core.models import SysUser, SysRole, SysDept, SysMenu, SysDictData, SysPost, SysDictType, SysConfig, SysNotice, \
    SysOperationLog, SysLoginLog


class LoginSerializer(JSONWebTokenSerializer):
    code = serializers.CharField()

    def validate_code(self, val):
        if val in cache:
           cache.delete(val)
        else:
            request = self.context['request']
            user_agent = parse(request.headers['User-Agent'])
            log = {
                'username': request.data.get('username'),
                'ip_addr': request.META['REMOTE_ADDR'],
                'login_location': '未知',
                'browser': user_agent.browser.family,
                'os': '%s %s' % (user_agent.os.family, user_agent.os.version[0]),
                'status': 1,
                'msg': '验证码错误'
            }
            SysLoginLog.objects.create(**log)
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }
        request = self.context['request']
        user_agent = parse(request.headers['User-Agent'])
        username = attrs.get('username')

        log = {
            'ip_addr': request.META['REMOTE_ADDR'],
            'login_location': '未知',
            'browser': user_agent.browser.family,
            'os': '%s %s' % (user_agent.os.family, user_agent.os.version[0])
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.status == '0':
                    msg = '账号已停用'
                    log['username'] = username
                    log['status'] = 1
                    log['msg'] = msg
                    SysLoginLog.objects.create(**log)
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)
                log['username'] = user.username
                log['status'] = 0
                log['msg'] = '登录成功'
                SysLoginLog.objects.create(**log)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = '用户名或密码错误'
                log['username'] = username
                log['status'] = 1
                log['msg'] = msg
                SysLoginLog.objects.create(**log)
                raise serializers.ValidationError(detail=msg)
        else:
            msg = '需同时提供用户名和密码'
            log['username'] = username
            log['status'] = 1
            log['msg'] = msg
            SysLoginLog.objects.create(**log)
            raise serializers.ValidationError(msg)

class SysPostSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysPost
        fields = '__all__'

class SysDeptSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysDept
        fields = '__all__'

class SysRoleSerializer(serializers.ModelSerializer):
    depts = SysDeptSerializer(read_only=True, many=True)
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysRole
        fields = '__all__'

class SysUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True, label='用户ID')
    dept = SysDeptSerializer(read_only=True, label='部门')
    username = serializers.CharField(required=True, allow_blank=False, allow_null=False, trim_whitespace=True, max_length=256, label='用户名称')
    nickname = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=256, label='用户昵称')
    password = serializers.CharField(required=False, allow_blank=True, allow_null=False, trim_whitespace=True, max_length=512, label='用户密码')
    email = serializers.EmailField(required=False, allow_blank=False, allow_null=True, trim_whitespace=True, max_length=128,label='邮箱')
    phone_number = serializers.CharField(required=False, allow_blank=False, allow_null=True, trim_whitespace=True, max_length=128, label='手机号码')
    sex = serializers.ChoiceField(required=True, choices=[('0', '男'), ('1', '女'), ('2', '未知')], label='用户性别')
    status = serializers.ChoiceField(required=True, choices=[('0', '正常'), ('1', '停用')], label='状态')
    remark = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=256, label='备注')
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    roles = SysRoleSerializer(many=True, read_only=True)
    posts = SysPostSerializer(many=True, read_only=True)


    def update(self, instance, validated_data):
        instance.nickname = validated_data['nickname']
        instance.email = validated_data['email']
        instance.phone_number = validated_data['phone_number']
        instance.sex = validated_data['sex']
        instance.status =  validated_data['status']
        instance.remark = validated_data['remark']
        instance.save()
        return instance

    def create(self, validated_data):
        user = SysUser.objects.create(**validated_data)
        return user

class SysMenuSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = SysMenu
        fields = '__all__'

class SysUserProfileSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    dept = SysDeptSerializer(read_only=True)
    roles = SysRoleSerializer(many=True, read_only=True)
    posts = SysPostSerializer(many=True, read_only=True)


    def create(self, validated_data):
        user = SysUser.objects.create(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.nickname = validated_data['nickname']
        instance.phone_number = validated_data['phone_number']
        instance.email = validated_data['email']
        instance.sex = validated_data['sex']
        instance.save()
        return instance

    class Meta:
        model = SysUser
        fields = ('user_id', 'dept', 'username', 'nickname', 'phone_number', 'email', 'sex', 'dept','roles', 'posts', 'status', 'create_time', 'update_time')

class SysUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs['old_password']
        new_password = attrs['new_password']

        if not user.check_password(old_password):
            print('原密码不正确')
            raise serializers.ValidationError('原密码不正确')

        if new_password == old_password:
            raise serializers.ValidationError('新密码不能与原密码相同')

        return {
            'old_password': old_password,
            'new_password': new_password
        }

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class SysDictDataSerializer(serializers.ModelSerializer):
    dict_type = serializers.PrimaryKeyRelatedField(queryset=SysDictType.objects.all())
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = SysDictData
        fields = '__all__'

class SysDictTypeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysDictType
        fields = '__all__'

class SysConfigSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysConfig
        fields = '__all__'

class SysNoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysNotice
        fields = '__all__'

class SysOperationLogSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysOperationLog
        fields = '__all__'

class SysLoginLogSerializer(serializers.ModelSerializer):
    login_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = SysLoginLog
        fields = '__all__'