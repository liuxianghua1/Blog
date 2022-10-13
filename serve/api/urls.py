from rest_framework.routers import DefaultRouter
from django.urls import path
from api import views

router = DefaultRouter()
router.register('users',views.UsersModelViewSet,basename="users")

urlpatterns = [
    path('login/', views.FormulaTokenObtainPairView.as_view(), name='login')
]


urlpatterns+=router.urls