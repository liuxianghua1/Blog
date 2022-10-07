from rest_framework.viewsets import ModelViewSet
from .models import Users
from .serializers import UsersSerializer

from rest_framework.pagination import PageNumberPagination

class MyPageNumberPagination(PageNumberPagination):
  page_size_query_param = "size"
  page_size = 10
  max_page_size = 50

class UsersModelViewSet(ModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UsersSerializer
  pagination_class = MyPageNumberPagination

