from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
  lastlogintime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
  
  class Meta:
    model = Users
    # fields = "__all__"
    fields = ["id","username","phone","createtime","lastlogintime","status","role"]