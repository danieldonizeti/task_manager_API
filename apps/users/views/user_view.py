from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.users.models import User
from apps.users.serializers.user_serializer import UserSerializer, CreateUserSerializer
from common.views.base_viewset import BaseModelViewSet
from ..serializers.user_serializer import ChangePasswordSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer
    

    @extend_schema(
            summary="Criar Usuario",
            description=(
                "Cria um novo usuario "
                "Preecha os campos completamente"
            ),
            request=CreateUserSerializer,
            responses={201: CreateUserSerializer},
        )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    
    @extend_schema(
                summary="Listar Usuarios",
                description=(
                    "Retorna os dados do proprio usuário autenticado."
                ),
            )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @extend_schema(
    summary="Dados do usuário logado",
    description="Retorna os dados do usuário autenticado.",
    responses={200: UserSerializer},
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


    @extend_schema(
        summary="Retorna o usuario autenticado",
        description=(
        "Retorna o usuario do ID informado na url desde que esteja autenticado"
        "Retorna 404 se o usuario não existir"
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary="Atualizar Usuario",
        description=(
            "Atualiza parcialmente um usuario autenticado. "
            "Todos os campos são opcicionais, envie apenas o que deseja alterar. "
            "Exceto os campos id e senha não saõ possiveis"
            "Retorna 404 se o usuario não existir"
        ),
        request=UserSerializer,
        responses={200: UserSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()

            return Response(
                {"message": "Senha alterada com sucesso"},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        summary="Alterar senha",
        description=(
            "Altera a senha do usuario autenticado. "
            "Informe a senha atual e a nova senha. "
        ),
        request=ChangePasswordSerializer,
        responses={200: None},
    )
    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)