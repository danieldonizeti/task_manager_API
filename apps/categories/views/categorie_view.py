from rest_framework import  permissions
from rest_framework.decorators import action
#from rest_framework.response import Response
from django.db.models import Q
from ..models import Category
from ..serializers.categories_serializer import CategorySerializer
from rest_framework.exceptions import PermissionDenied
from common.views.base_viewset import BaseModelViewSet
from ..permissions import IsNotSystemCategory


class CategoryViewSet(BaseModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsNotSystemCategory]

    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        
        return Category.objects.filter(
            Q(user__isnull=True) | Q(user=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)