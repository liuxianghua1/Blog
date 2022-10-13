from rest_framework import serializers
from serve.settings import SIMPLE_JWT ,SECRET_KEY
from api.models import Users
from jwt import decode as jwt_decode
from django.utils import timezone as datetime



class TokenAuth:

    # 自定义 JWT Token 认证类

    @staticmethod
    def authenticate(request):
        # 获取请求头的 Authorization 字段
        headers_token = request.headers.get('Authorization', None)


        # 校验 Authorization 是否符合规范
        jwt = SIMPLE_JWT['JWT_AUTH_HEADER_PREFIX']
        if not headers_token:
            raise serializers.ValidationError({'Authorization': '该字段是必填项。'})
        elif headers_token.find(jwt + ' ') == -1:
            raise serializers.ValidationError({'Token': '该字段不符合规范。'})


        # 提取 Authorization 中的 JWT Token 信息
        headers_token = headers_token.split(jwt + ' ')[1]
        print(headers_token)
        
        decoded_data = jwt_decode(headers_token, SECRET_KEY, algorithms=["HS256"])
        checkUser = Users.objects.filter(id=decoded_data.get('user_id'),username=decoded_data.get('name'))

        # 每次用户调用接口都会更新一次他的最后使用时间
        checkUser.update(lastlogintime=datetime.now())

        if checkUser:
          return checkUser,"1"
        #   return checkUser,headers_token 应该返回这个


