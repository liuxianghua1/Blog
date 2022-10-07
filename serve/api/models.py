from random import choices
from django.db import models

# Create your models here.

class Users(models.Model):
  # 用户命、密码、手机号、创建时间、最近登录时间、权限、token、状态
  role_choices = (
    (0,"管理员"),
    (1,"超级管理员")
  )
  status_choices = (
    (0,"禁用"),
    (1,"激活")
  )

  username = models.CharField(max_length=32, unique = True)
  password = models.CharField(max_length=32)
  phone = models.CharField(max_length=32)
  createtime = models.DateField()
  lastlogintime = models.DateField()
  role = models.SmallIntegerField(choices=role_choices,default=0)
  token = models.CharField(max_length=64, null=True, blank=True)
  status = models.SmallIntegerField(choices=status_choices, default=1)

