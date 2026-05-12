#from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


from apps.tasks.models import Task
from apps.tasks.serializers.task_serializer import TaskSerializer
from common.permissions.is_owner import IsOwner
#from common.utils.response import success_response
from common.views.base_viewset import BaseModelViewSet


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