
from rest_framework import serializers
from .models import Users



class UsersSerializer(serializers.ModelSerializer):
  lastlogintime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
  password =  serializers.CharField(write_only=True)
  # 这个意思是不展示这个数据 但是提交得填这个数据还是会被修改

  class Meta:
    model = Users
    fields = "__all__"
    # fields = ["id","username","phone","createtime","lastlogintime","status","role"]
    # 查询这里可以不用改 密码永远不能显示出来

    
 

    

      

      