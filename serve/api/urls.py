from rest_framework.routers import DefaultRouter
from django.urls import path
from api import views

router = DefaultRouter()
router.register('users',views.UsersModelViewSet,basename="users")
router.register('articles',views.ArticlesModelViewSet,basename="articles")
router.register('categorys',views.CategorysModelViewSet,basename="category")
# router.register('categorys',views.WebArticleListModelMixin,basename="category")



urlpatterns = [
    path('login/', views.FormulaTokenObtainPairView.as_view(), name='login'),
    path('update_pass/', views.UpdatePassView.as_view(), name='update_pass'),
    path('article_list/', views.WebArticleListModelMixin.as_view({"get": "list"}), name='article_list'),
    path('article_list/<int:pk>/', views.WebArticleListModelMixin.as_view({"get": "retrieve"})),
    path('category_list/<int:pk>/', views.WebCategoryListModelmixin.as_view({"get": "retrieve"})),
    path('category_list/', views.WebCategoryListModelmixin.as_view({"get": "list"})),
    path('archiving/', views.WebarchivingListModelMixin.as_view({"get": "list"})),
]


urlpatterns+=router.urls