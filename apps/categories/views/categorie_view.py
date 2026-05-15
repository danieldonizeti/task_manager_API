from rest_framework import permissions
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from ..models import Category
from ..serializers.categories_serializer import CategorySerializer
from ..permissions import IsNotSystemCategory

from common.views.base_viewset import BaseModelViewSet

import logging

logger = logging.getLogger(__name__)


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
        category = serializer.save(user=self.request.user)

        logger.info(
            {
                "event": "category_created",
                "user_id": self.request.user.id,
                "category_id": category.id,
                "path": self.request.path,
                "method": self.request.method,
            },
            extra={
                "request_id": self.request.request_id
            }
        )
    
    def perform_destroy(self, instance):

        logger.warning(
            {
                "event": "category_deleted",
                "user_id": self.request.user.id,
                "category_id": instance.id,
                "path": self.request.path,
                "method": self.request.method,
            },
            extra={
                "request_id": self.request.request_id
            }
        )
        instance.delete()