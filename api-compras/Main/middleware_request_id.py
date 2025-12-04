# Main/middleware_request_id.py
import uuid
import time
import logging
from django.utils.deprecation import MiddlewareMixin
from .logging_filters import set_request_context

logger = logging.getLogger("app")

class RequestContextMiddleware(MiddlewareMixin):
    def process_request(self, request):
        req_id = str(uuid.uuid4())
        user_id = "-"
        if hasattr(request, "user") and getattr(request.user, "is_authenticated", False):
            user_id = str(getattr(request.user, "pk", "-"))
        set_request_context(req_id, user_id)
        request._start_time = time.time()
        logger.info("➡️ %s %s", request.method, request.path)

    def process_response(self, request, response):
        try:
            duration_ms = int((time.time() - getattr(request, "_start_time", time.time())) * 1000)
        except Exception:
            duration_ms = -1
        logger.info("✅ %s %s %s (%d ms)", request.method, request.path, getattr(response, "status_code", "?"), duration_ms)
        return response

    def process_exception(self, request, exception):
        logger.exception("💥 Error no manejado: %s", str(exception))
        return None
