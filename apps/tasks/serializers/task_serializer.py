from rest_framework import serializers
from apps.tasks.models import Task
from django.utils.timezone import now


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    priority_code = serializers.CharField(
        source='get_priority_code',
        read_only=True
    )

    priority_display = serializers.CharField(
        source='get_priority_display',
        read_only=True
    )


    title = serializers.CharField(
        error_messages={
            "required": "O titulo é obrigatório.",
            "blank": "O titulo não pode ser vazio"
        }
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',         
            'priority_code',
            'priority_display',  
            'created_at',
            'updated_at',
            'due_date',
            'user'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
    
    
    def validate_due_date(self, value):
        if value and value < now():
            raise serializers.ValidationError("A data deve ser superior ao dia de hoje")
        return value


    def validate_status(self, value):
        if self.instance and self.instance.status == 'concluída' and value != 'concluída':
            raise serializers.ValidationError(
                "Não é possível alterar o status de uma tarefa concluída."
            )
        return value

    # conversão de entrada
    def to_internal_value(self, data):
        data = data.copy()

        if "priority" in data:
            raw = data["priority"]

            # já é número
            if isinstance(raw, int):
                pass
            else:
                val = str(raw).lower().strip()

                pt_map = {
                    "baixa": "baixa",
                    "media": "media",
                    "média": "media",
                    "alta": "alta"
                }

                val = pt_map.get(val, val)

                code_map = Task.PRIORITY_CODE_MAP

                if val in code_map:
                    data["priority"] = code_map[val]
                else:
                    raise serializers.ValidationError({
                        "priority": "Use: baixa, media, alta ou 1,2,3"
                    })

        return super().to_internal_value(data)