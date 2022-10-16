from rest_framework import mixins,viewsets,generics
from .models import Users,Article,Category
from .serializers import UsersSerializer,MyTokenObtainPairSerializer,ArticleSerializer,CategorysSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import BasePermission
from django.utils import timezone as datetime
import random
# 图片上传
from rest_framework.parsers import MultiPartParser,JSONParser,FormParser

# 分页类
class MyPageNumberPagination(PageNumberPagination):
  page_size_query_param = "size"
  page_size = 10
  max_page_size = 50

# 提供分类
class CategorysModelViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
  queryset = Category.objects.all().order_by("id")
  serializer_class = CategorysSerializer

  @action(methods=["post"],detail=False)
  def create_category(self, request):
      name = request.data.get('name')
      nameExist = Category.objects.filter(name=name)

      if nameExist:
        return Response({'msg':'分类名已存在','code':500})
      else:
        ser = CategorysSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"code": 400, "data": ser.errors})
        ser.save()
        return Response({'msg':'添加成功','code':200})


  @action(methods=["put"],detail=True)
  def update_category(self, request,pk):
      name = request.data.get('name')
      nameExist = Category.objects.filter(name=name)

      if nameExist:
        return Response({'msg':'分类名已存在','code':500})
      else:
        ser = CategorysSerializer(Category.objects.filter(id=pk).first(),data=request.data)
        if not ser.is_valid():
            return Response({"code": 400, "data": ser.errors})
        ser.save()
        return Response({'msg':'更新成功','code':200})


# 文章类
class ArticlesModelViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
  queryset = Article.objects.all().order_by("-id","createtime","title")
  serializer_class = ArticleSerializer
  pagination_class = MyPageNumberPagination
  parser_classes = [JSONParser,FormParser,MultiPartParser]

  # 文章发布方法
  @action(methods=["post"],detail=False)
  def create_article(self,request):
    request.data['author_id'] = request.user[0].id
    request.data['image_url'] = request.data['image_name']
    request.data['categorys'] = request.data['categorysList']
    ser = ArticleSerializer(data=request.data)
    if not ser.is_valid():
        return Response({"code": 400, "data": ser.errors})
    ser.save()
    return  Response({'msg':"文章发布成功",'code':200})
    

   # 更新方法
  @action(methods=["put"],detail=True)
  def update_article(self, request,pk):
      status = request.data.get('status')
      article = Article.objects.filter(id=pk)
      if len(request.data) == 1 and status in [0,1]:
        article.update(status=status)
        return Response({'msg':'状态修改成功','code':201})
      else:
        image_url = request.data.get('image_url').split("/")[-1]
        title = request.data.get('title')
        body = request.data.get('body')
        categorys = request.data.get('categorysList')
        data={
          'image_url':image_url,'title':title,'body':body,'categorys':categorys,'status':status,'author_id':request.user[0].id
        }
        ser = ArticleSerializer(article.first(),data=data)
        if not ser.is_valid():
          return Response({"code": 400, "data": ser.errors})
        ser.save()
        return Response({'msg':'修改成功','code':200})

  # 图片上传方法
  @action(methods=["post"],detail=False)
  def image_upload(self,request):
    img = request.data.get("file")
    img_type = img.name.split('.')[-1]
    if img_type not in['png', 'jpg', 'jpeg']:
      return  Response({'msg':"上传图片类型不正确",'code':500})
    newfielname = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(10000,99999)) + '.' + img_type  #采用时间和随机数重命名图片
    path = "../admin/public/uploads/" +newfielname
    with open(path,'wb') as f:  #二进制写入
                for i in img.chunks():
                    f.write(i)
    return  Response({'msg':"成功",'code':200,"filename":newfielname})



 

# token类
class FormulaTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# 权限类
class SuperAdminPermission(BasePermission):
  message = {"code": 500, 'msg': "无权访问"}
  def has_permission(self, request, view):
      if request.user[0].role == 1:
            return True
      return False

# 用户视图
class UsersModelViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
  permission_classes = [SuperAdminPermission]
  queryset = Users.objects.all().order_by("-lastlogintime",)
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
      user = Users.objects.filter(id=pk)
     
      # 这是用户列表中滑块修改状态的方法判断
      if len(request.data) == 1 and status in [0,1]:
        user.update(status=status)
        return Response({'msg':'状态修改成功','code':201})
      
      user.update(status=status, password=password, role=role)
      return Response({'msg':'修改成功','code':201})
      
    

class UpdatePassView(generics.GenericAPIView):
  def put(self, request, *args, **kwargs):
    pk = request.user[0].id
    user = Users.objects.filter(id= pk)
    oldPassword = request.data.get('oldPassword')
    password = request.data.get('password')
    check = check_password(oldPassword,user.first().password)
    if check:
      user.update(password=make_password(password))
      return Response({'msg':'修改成功','code':200})
    else:
      return Response({'msg':'原密码不正确','code':500})
  




