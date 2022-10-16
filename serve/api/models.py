from django.db import models


# 用户模型
class Users(models.Model):
  # 用户命、密码、手机号、创建时间、最近登录时间、权限、token、状态
  role_choices = (
    (0,"管理员"),
    (1,"超级管理员")
  )
  status_choices = (
    (0,"禁用"),
    (1,"激活")
  )

  username = models.CharField(max_length=32, unique = True)
  password = models.CharField(max_length=256)
  phone = models.CharField(max_length=32)
  createtime = models.DateField(auto_now_add=True)
  lastlogintime = models.DateTimeField(null=True,blank=True)
  role = models.SmallIntegerField(choices=role_choices,default=0)
  status = models.SmallIntegerField(choices=status_choices, default=1)

  def is_authenticated(self):
      return True

'''
文章表
id 作者 发布时间 浏览量 
id author createtime pageview title body
1  刘翔華  2022-10-14 10      
4  刘翔華  2022-10-14 10      
5  刘翔華  2022-10-14 10      


分类表
id name
1   web
2   python
3   vue

这样就表名 id为1的文章关联到分类表1和3 vue 和 web
这样就表名 id为4的文章关联到分类表2 python

分类文章关联表
id article_id category_id
1   1       1
2   1       3
3   4       2
4   5       2

分类文章关联表的article 对应文章表的id category 对应分类表的id 多对多
'''



# 多对多
# roles = models.ManyToManyField(verbose_name="角色", to="Role
# 文章模型
class Article(models.Model):


    # id author createtime clicks title body category
    # CASCADE       :主表删除，从表全部删除
    # SET_NULL      :主表删除后，从表设置为NULL

    status_choices = (
    (0,"隐藏"),
    (1,"展示")
    )

    createtime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64,null=True,blank=True)
    body = models.TextField(null=True,blank=True)
    # 文章封面图
    image_url = models.CharField(null=True,blank=True,max_length=64)
    clicks = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=status_choices, default=1)
    author = models.ForeignKey(to='Users',to_field='id',on_delete=models.SET_NULL,null=True)

    categorys = models.ManyToManyField("Category",db_table="db_article2category")
    related_name="category_list"


# 分类模型 # 文章分类多对多模型自动创建
class Category(models.Model):
    name = models.CharField(max_length=32)




# 留言表