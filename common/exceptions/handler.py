from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    #Erros tratados pelo DRF (validação, permissão, etc)
    if response is not None:
        return Response({
            "success": False,
            "error": response.data,
            "message": "Erro na requisição"
        }, status=response.status_code)

    #Erros que são inesperados exemplo (500)
    return Response({
        "sucess": False,
        "message": "Erro interno do servidor"
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)