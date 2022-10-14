from rest_framework import serializers #序列化器
from .models import Users,Article,Category   #用户模型
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #jwt
from django.utils import timezone as datetime
from django.contrib.auth.hashers import check_password #密码解码



# 用户序列化器
class UsersSerializer(serializers.ModelSerializer):
  lastlogintime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
  password =  serializers.CharField(write_only=True)
  # 这个意思是不展示这个数据 但是提交得填这个数据还是会被修改

  class Meta:
    model = Users
    fields = "__all__"
    # fields = ["id","username","phone","createtime","lastlogintime","status","role"]
    # 查询这里可以不用改 密码永远不能显示出来

    def get_username(self,obj):
        #  返回 obj对象中调用外键kind中的school_name字段 (学校表中school_name学校名称)
        return obj.username

# 分类序列化器
class CategorysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# 文章序列化器
class ArticleSerializer(serializers.ModelSerializer):
    categorys = CategorysSerializer(many=True)
    author = serializers.CharField(source='author.username',read_only=True)
    author_role = serializers.IntegerField(source='author.role',read_only=True)
    author_id = serializers.IntegerField(source='author.id',read_only=True)
    createtime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = Article
        fields = "__all__"
 
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
                if user.status == 1:
                    #给登录的用户附上登录时间
                    Users.objects.filter(id=user.id).update(lastlogintime=datetime.now())
                    data = {"msg":"登陆成功","role":user.role,"code":200,"username":user.username,"id": user.id, "token": str(refresh.access_token), "refresh": str(refresh)}
                    return data
                else:
                    return {"msg":'你的账号被禁止登录',"code":500}
            return {"msg":'账号或密码错误',"code":500}
        except Exception as e:
            return {"msg":e.args[0],"code":500}