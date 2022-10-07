from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register('users',views.UsersModelViewSet,basename="users")

urlpatterns = [
    
]


urlpatterns+=router.urls