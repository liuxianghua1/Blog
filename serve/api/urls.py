from rest_framework.routers import DefaultRouter
from django.urls import path
from api import views

router = DefaultRouter()
router.register('users',views.UsersModelViewSet,basename="users")
router.register('articles',views.ArticlesModelViewSet,basename="articles")
router.register('categorys',views.CategorysModelViewSet,basename="category")



urlpatterns = [
    path('login/', views.FormulaTokenObtainPairView.as_view(), name='login'),
    path('update_pass/', views.UpdatePassView.as_view(), name='update_pass')
]


urlpatterns+=router.urls