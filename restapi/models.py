# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UserBlack(models.Model):
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_black'


class UserGroup(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_group'


class UserInfo(models.Model):
    user_type = models.IntegerField()
    user_name = models.CharField(max_length=32)
    password = models.CharField(max_length=100)
    group_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'


class UserRole(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_role'


class UserToken(models.Model):
    user_id = models.IntegerField()
    user_token = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user_token'


class UserinfoRoles(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userinfo_roles'
