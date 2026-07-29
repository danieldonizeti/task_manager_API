from rest_framework import permissions
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from ..models import Category
from ..serializers.categories_serializer import CategorySerializer
from ..permissions import IsNotSystemCategory

from common.views.base_viewset import BaseModelViewSet
from common.audit.logger import audit_log

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


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
        ).order_by('-id')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    def perform_destroy(self, instance):
        instance.delete()


    @extend_schema(
        summary="Criar categoria",
        description=(
            "Cria uma nova categoria vinculada ao usuário autenticado. "
            "Categorias com nome igual ao do sistema não podem ser criadas por usuários. "
        ),
        request=CategorySerializer,
        responses={201: CategorySerializer},
        )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary="Listar categorias",
        description=(
            "Retorna uma lista paginada das categorias do usuario autenticado e categorias do sistema. "
        ),
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary="Exibir uma categoria especifica",
        description=(
            "Retorna uma categoria do usuario autenticado ou uma do sistema. "
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary="Atualizar uma Categoria",
        description=(
                "Atualiza o nome de uma categoria do usuario autenticado. "
                "Somente categorias do usuario, do sistema não imutaveis. "
        ),
        request=CategorySerializer,
        responses={200: CategorySerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @extend_schema(
            summary="Deletar Categoria",
            description=(
                "Remove permanentemente uma Categoria do usuario autenticado. "
                "Essa ação não pode ser desfeita. "
                "Retorna 404 se a categoria não existir ou não pertencer ao usuario. "
            ),
            responses={204: None},
        )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)