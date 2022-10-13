from rest_framework import serializers
from serve.settings import SIMPLE_JWT as JWT_AUTH,SECRET_KEY
from api.models import Users
from jwt import decode as jwt_decode



class TokenAuth:

    # 自定义 JWT Token 认证类

    @staticmethod
    def authenticate(request):

        # 获取请求头的 Authorization 字段
        headers_token = request.headers.get('Authorization', None)
        # 校验 Authorization 是否符合规范
        if not headers_token:
            raise serializers.ValidationError({'Authorization': '该字段是必填项。'})
        elif headers_token.find(JWT_AUTH['JWT_AUTH_HEADER_PREFIX'] + ' ') == -1:
            raise serializers.ValidationError({'Token': '该字段不符合规范。'})
        # 提取 Authorization 中的 JWT Token 信息
        headers_token = headers_token.split(JWT_AUTH['JWT_AUTH_HEADER_PREFIX'] + ' ')[1]
        # 调用默认的验证逻辑
        decoded_data = jwt_decode(headers_token, SECRET_KEY, algorithms=["HS256"])
        checkUser = Users.objects.filter(id=decoded_data.get('user_id'),username=decoded_data.get('name'))
        if checkUser:
          return checkUser,"ok"


