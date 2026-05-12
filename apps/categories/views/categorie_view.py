from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from ..models import Category
from ..serializers.categories_serializer import CategorySerializer
from rest_framework.exceptions import PermissionDenied
from common.views.base_viewset import BaseModelViewSet


class CategoryViewSet(BaseModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        return Category.objects.filter(
            Q(user__isnull=True) | Q(user=user)
        )
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        if serializer.instance.is_system:
            raise PermissionDenied("Não é permitido editar categorias do sistema.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.is_system:
            raise PermissionDenied("Não é permitido excluir categorias do sistema.")
        instance.delete()