from rest_framework import viewsets
from common.utils.response import success_response


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
        return success_response(
            response.data,
            self.success_messages["create"],
            201
        )
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return success_response(
            response.data,
            self.success_messages["update"]
        )
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return success_response(
            message=self.success_messages["destroy"]
        )