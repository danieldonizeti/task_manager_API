from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.auth_view import CustomTokenObtainPairView

from apps.users.views.user_view import ChangePasswordView

from .views import api_root

from apps.users.views.user_view import UserViewSet
from apps.tasks.views.task_view import TaskViewSet
from apps.categories.views.category_view import CategoryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', api_root, name='api-home'),

    path('admin/', admin.site.urls),

    path('api/users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('api/', include(router.urls)),

    path('api/auth/login/', CustomTokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),

    #Minhas rotas de documentação
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]