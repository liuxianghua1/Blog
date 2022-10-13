from urllib import request
from rest_framework import mixins,viewsets
from .models import Users
from .serializers import UsersSerializer,MyTokenObtainPairSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import BasePermission

class FormulaTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyPageNumberPagination(PageNumberPagination):
  page_size_query_param = "size"
  page_size = 10
  max_page_size = 50

class SuperAdminPermission(BasePermission):
  message = {"code": 500, 'msg': "无权访问"}
  def has_permission(self, request, view):
      if request.user[0].role == 1:
            return True
      return False


class UsersModelViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
  permission_classes = [SuperAdminPermission]
  queryset = Users.objects.all().order_by("-id")
  serializer_class = UsersSerializer
  pagination_class = MyPageNumberPagination

  
  # 自定义创建用户方法
  # 创建用户应该重写create这个方法 用户名和手机号需要进行查重 并且密码要进行加密
  @action(methods=["post"],detail=False)
  def createuser(self, request):
      username = request.data.get('username')
      phone = request.data.get('phone')
      usernameExist = Users.objects.filter(username=username)
      phoneExist = Users.objects.filter(phone=phone)

      if usernameExist:
        return Response({'msg':'用户名已存在','code':500})
      elif phoneExist:
        return Response({'msg':'手机号已存在','code':500})
      else:
        request.data['password'] = make_password(request.data.get('password'))
        ser = UsersSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 400, "data": ser.errors})
        ser.save()
        return Response({'msg':'添加成功','code':201})
   

  # 自定义更新方法
  # 更新用户也是 密码需要进行加密 用户名和手机号不允许传参过来 只修改密码和权限、状态
  @action(methods=["put"],detail=True)
  def updateuser(self, request,pk):
      status = request.data.get('status')
      password = make_password(request.data.get('password'))
      role = request.data.get('role')
      if len(request.data) == 1 and status in [0,1]:
        Users.objects.filter(id=pk).update(status=status)
        return Response({'msg':'修改成功','code':201})

      # print(check_password('123',make_password('123')))
      # 密码解码用

      Users.objects.filter(id=pk).update(status=status, password=password, role=role)
      return Response({'msg':'修改成功','code':201})
      
    
