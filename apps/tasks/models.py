from django.db import models
from django.conf import settings


class Task(models.Model):

    class PriorityChoices(models.IntegerChoices):
        LOW = 1, 'Baixa'
        MEDIUM = 2, 'Media'
        HIGH = 3, 'Alta'
    
    PRIORITY_CODE_MAP = {
        'baixa': PriorityChoices.LOW,
        'media': PriorityChoices.MEDIUM,
        'alta': PriorityChoices.HIGH
    }

    PRIORITY_REVERSE_CODE_MAP = {v: k for k, v in PRIORITY_CODE_MAP.items()}
    
    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM
    )

    def get_priority_display(self):
        return self.PRIORITY_REVERSE_CODE_MAP.get(self.priority)
    

    class StatusChoices(models.TextChoices):
        PENDING = 'pendente', 'Pendente'
        IN_PROGRESS = 'em progresso', 'Em Progresso'
        DONE = 'concluída', 'Concluída'

    
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title