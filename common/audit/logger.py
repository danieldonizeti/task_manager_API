import logging


logger = logging.getLogger(__name__)


def audit_log(
        *,
        event,
        request,
        level="info",
        **kwargs
):
    data={
        "event": event,
        "user_id": (
            request.user.id
            if request.user.is_authenticated
            else None
        ),
        "path": request.path,
        "method": request.method,
        **kwargs
    }

    extra = {
        "request_id": getattr(
            request,
            "request_id",
            "unknown"
        )
    }

    log_method = getattr(logger, level)
    log_method(event, extra={**data, **extra})
