from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    request = context.get("request")

    request_id = getattr(request, "request_id", "unknown")

    # erros tratados pelo DRF
    if response is not None:

        logger.warning(
            {
                "event": "handled_exception",
                "status_code": response.status_code,
                "path": request.path if request else None,
                "method": request.method if request else None,
            },
            extra={
                "request_id": request_id
            }
        )

        return Response(
            {
                "success": False,
                "error": response.data,
                "request_id": request_id,
            },
            status=response.status_code
        )

    # erros inesperados
    logger.exception(
        {
            "event": "unhandled_exception",
            "path": request.path if request else None,
            "method": request.method if request else None,
        },
        extra={
            "request_id": request_id
        }
    )

    return Response(
        {
            "success": False,
            "message": "Erro interno do servidor",
            "request_id": request_id,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )