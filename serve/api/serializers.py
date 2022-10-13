from rest_framework import serializers #序列化器
from .models import Users   #用户模型
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #jwt
from rest_framework import exceptions #异常报错
from django.contrib.auth.hashers import check_password #密码解码

class UsersSerializer(serializers.ModelSerializer):
  lastlogintime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
  password =  serializers.CharField(write_only=True)
  # 这个意思是不展示这个数据 但是提交得填这个数据还是会被修改

  class Meta:
    model = Users
    fields = "__all__"
    # fields = ["id","username","phone","createtime","lastlogintime","status","role"]
    # 查询这里可以不用改 密码永远不能显示出来


 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # 自定义登录认证，使用自有用户表

    def validate(self, attrs):
        try:
            user = Users.objects.get(username= attrs['username'])

            check = check_password(attrs['password'],user.password)
            # 对密码进行解密 如果密码正确则发送token 否则报错

            if check:
                refresh = self.get_token(user)
                refresh["name"] = user.username
                refresh["role"] = user.role
                refresh["status"] = user.status
                if user.status == 0:
                    return {"msg":'你的账号被禁止登录',"code":500}
                data = {"msg":"登陆成功","code":200,"id": user.id, "token": str(refresh.access_token), "refresh": str(refresh)}
                return data
            return {"msg":'账号或密码错误',"code":500}
        except Exception as e:
            # raise exceptions.NotFound(e.args)
            return {"msg":e.args[0],"code":500}