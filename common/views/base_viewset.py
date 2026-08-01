from rest_framework import viewsets

from common.utils.response import success_response
from common.audit.logger import audit_log

from drf_spectacular.utils import extend_schema

class BaseModelViewSet(viewsets.ModelViewSet):

    success_messages = {
        "list": "Lista retornada com sucesso",
        "retrieve": "Recurso encontrado",
        "create": "Recurso criado com sucesso",
        "update": "Recurso atualizado com sucesso",
        "destroy": "Recurso deletado com sucesso",
    }

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return success_response(
            response.data,
            self.success_messages["list"]
        )
    
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return success_response(
            response.data,
            self.success_messages["retrieve"]
        )
    
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        audit_log(
            event="recurso_criado",
            request=request,
            obj_id=response.data.get("id") if isinstance(response.data, dict) else None,
            resource=self.basename,
            fields=list(request.data.keys())
        )

        return success_response(
            response.data,
            self.success_messages["create"],
            201
        )
    
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        audit_log(
            event="recurso_atualizado",
            request=request,
            obj_id=response.data.get("id") if isinstance(response.data, dict) else None,
            resource=self.basename,
            fields=list(request.data.keys())
        )

        return success_response(
            response.data,
            self.success_messages["update"],
            201
        )
    
    def destroy(self, request, *args, **kwargs):
        object_id = kwargs.get("pk")

        super().destroy(request, *args, **kwargs)

        audit_log(
            event="recurso_deletado",
            request=request,
            obj_id=object_id,
            resource=self.basename,
        )

        return success_response(
            message=self.success_messages["destroy"]
        )

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)