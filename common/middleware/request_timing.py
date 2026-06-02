import time
import logging

logger = logging.getLogger("request_timing")


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    

    def __call__(self, request):
        start =  time.perf_counter()

        response = self.get_response(request)

        duration_ms = int((time.perf_counter() - start) * 1000)

        if not request.path.startswith("/admin/"):
            user = getattr(request, "user", None)

            logger.info(
                "request_completed",
                extra={
                    "request_id": getattr(request, "request_id", "unknown"),
                    "path": request.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "user_id": getattr(user, "id", None),
                }
            )
        
        response["X-Response-Time-ms"] = str(duration_ms)
        return response