from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    # fields = "__all__"
    fields = ["id","username","phone","createtime","lastlogintime","status","role"]