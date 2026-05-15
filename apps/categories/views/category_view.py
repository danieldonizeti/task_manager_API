from rest_framework import permissions
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from ..models import Category
from ..serializers.categories_serializer import CategorySerializer
from ..permissions import IsNotSystemCategory

from common.views.base_viewset import BaseModelViewSet
from common.audit.logger import audit_log


class CategoryViewSet(BaseModelViewSet):

    permission_classes = [
        permissions.IsAuthenticated,
        IsNotSystemCategory
    ]

    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        
        return Category.objects.filter(
            Q(user__isnull=True) | Q(user=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    def perform_destroy(self, instance):
        instance.delete()