#from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


from apps.tasks.models import Task
from apps.tasks.serializers.task_serializer import TaskSerializer
from common.permissions.is_owner import IsOwner
#from common.utils.response import success_response
from common.views.base_viewset import BaseModelViewSet

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class TaskViewSet(BaseModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['status', 'priority']
    ordering_fields = ['created_at', 'priority', 'status']
    ordering = ['created_at']
    search_fields = ['title']

    success_messages = {
        "list": "Lista de tarefas",
        "retrieve": "Detalhes da tarefa",
        "create": "Tarefa criada com sucesso",
        "update": "Tarefa atualizada com sucesso",
        "destroy": "Tarefa removida com sucesso"
    }

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).select_related('user')
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
    @extend_schema(
        summary="Listar tarefas",
        description=(
            "Retorna uma lista paginada de todas as tarefas do usuario autenticado"
            "Suporta filtros por status e prioridades, além de ordenação e busca por titulo"
        ),
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filtra por status. Valores: pendente, em progresso, concluida",
                required=False,
            ),OpenApiParameter(
                name="priority",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filtra por prioridade. Valores: 1 (baixa), 2 (média), 3 (alta)",
                required=False,
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Ordena os resultados. Valores: created_at, priority, status. Use - para ordem decrescente. Ex: -priority",
                required=False,
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Busca tarefas pelo título",
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @extend_schema(
        summary="Detalhar uma tarefa",
        description=(
            "Retorna os detalhes de uma tarefa especifica do usuario autenticado"
            "Retorna 404 se a tarefa não existir ou não pertencer ao usuario"
        ),
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
        summary="Criar tarefa",
        description=(
            "Cria uma nova tarefa vinculada ao usuario autenticado. "
            "O campo 'user' é preenchido automaticamente. "
            "A prioridade aceita tanto numeros (1,2,3) quanto texto (baixa, media, alta).   "
            "A data de vencimento não pode ser uma data no passado"
        ),
        request=TaskSerializer,
        responses={201: TaskSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @extend_schema(
        summary="Atualizar tarefa",
        description=(
            "Atualiza parcialmente uma tarefa existente do usuario autenticado. "
            "Todos os campos são opicionais envie apenas o que deseja alterar. "
            "Não é possivel alterar o status de uma tarefa já concluida. "
            "Retorna 404 se a tarefa não existir ou não pertencer ao ususario"
        ),
        request=TaskSerializer,
        responses={200: TaskSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @extend_schema(
        summary="Deletar tarefa",
        description=(
            "Remove permanentemente uma terefa do usuario autenticado. "
            "Essa ação não pode ser desfeita. "
            "Retorna 404 se a tarefa não existir ou não pertencer ao usuario."
        ),
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)