from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.auth_view import CustomTokenObtainPairView
from .views import api_root

from apps.users.views.user_view import UserViewSet
from apps.tasks.views.task_view import TaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet, basename='tasks')


urlpatterns = [
    path('', api_root, name='api-home'),

    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('api/auth/login/', CustomTokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    ]