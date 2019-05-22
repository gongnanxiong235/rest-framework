from rest_framework import serializers
from restapi import models

# 可以对序列化字段的值进行加工和定制  == user_name = serializers.CharField()
class MyField(serializers.CharField):
    def to_representation(self, value):
        if value == 'gongnanxiong':
            return 'shuaige:' + value
        return value


# 序列化 方式1
class UserInfoSerializers(serializers.Serializer):
    user_id = serializers.IntegerField(source='id')
    # user_type=serializers.ChoiceField(choices=((1,'普通用户'),(2,'VIP用户'),(3,'超级VIP 用户')))
    user_type = serializers.SerializerMethodField()
    # user_name = serializers.CharField()
    user_name = MyField()
    group_name = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    def get_roles(self, obj):
        role_name = list()
        user_id = obj.id
        role_ids = models.UserinfoRoles.objects.filter(user_id=user_id).values('role_id')
        for rid in role_ids:
            role_obj = models.UserRole.objects.filter(id=rid.get('role_id')).first()
            role_name.append(role_obj.title)
        return role_name

    def get_user_type(self, obj):
        type = obj.user_type
        if type == 1:
            return '普通用户'
        elif type == 2:
            return 'vip用户'
        elif type == 3:
            return ' 超级VIP用户'

    def get_group_name(self, obj):
        print('obj', obj)
        if obj.group_id:
            print(obj.id)
            group = models.UserGroup.objects.filter(id=obj.group_id).first()
            if group:
                return {"id": group.id, 'title': group.title}
        return None


# 序列化 方式2
class UserInfoSerializers2(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        # fields = "__all__"
        fields = ['id', 'user_name', 'user_type', 'group_name', 'roles']
        # depth = 1   有关联关系的自动查询

    def get_roles(self, obj):
        role_name = list()
        user_id = obj.id
        role_ids = models.UserinfoRoles.objects.filter(user_id=user_id).values('role_id')
        for rid in role_ids:
            role_obj = models.UserRole.objects.filter(id=rid.get('role_id')).first()
            role_name.append(role_obj.title)
        return role_name

    def get_user_type(self, obj):
        type = obj.user_type
        if type == 1:
            return '普通用户'
        elif type == 2:
            return 'vip用户'
        elif type == 3:
            return ' 超级VIP用户'

    def get_group_name(self, obj):
        print('obj', obj)
        if obj.group_id:
            print(obj.id)
            group = models.UserGroup.objects.filter(id=obj.group_id).first()
            print(obj.group_id)
            if group:
                return {"id": group.id, 'title': group.title}
        return None

# 序列化 方式3  反向生成url的方式
class UserInfoSerializers3(serializers.ModelSerializer):
    # lookup_field='group_id',lookup_url_kwarg='pk':按照对用的group_id去生成url  如果不写 默认按照userinfo的id来生成
    group = serializers.HyperlinkedIdentityField(view_name='gp', source='group_id', lookup_field='group_id',
                                                 lookup_url_kwarg='pk')

    class Meta:
        model = models.UserInfo
        fields = "__all__"


class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = "__all__"


class RoleSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


#  分页
class RoleSer(serializers.ModelSerializer):
    class Meta:
        model = models.UserRole
        fields = "__all__"