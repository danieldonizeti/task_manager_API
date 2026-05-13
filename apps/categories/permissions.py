from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotSystemCategory(BasePermission):
    """
    Permissão personalizada para impedir a edição ou exclusão de categorias do sistema.
    """

    message = "Não é permitido modificar categorias do sistema."

    def has_object_permission(self, request, view, obj):
        #Estou permitindo apenas métodos seguros GET, HEAD, OPTIONS para categorias do sistema
        if request.method in SAFE_METHODS:
            return True
        
        return not obj.is_system