# Main/logging_filters.py
import logging
import threading

_thread_local = threading.local()

def set_request_context(request_id: str = "-", user_id: str = "-"):
    _thread_local.request_id = request_id or "-"
    _thread_local.user_id = user_id or "-"

class RequestContextFilter(logging.Filter):
    """Inyecta request_id y user_id desde thread-local a cada log."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = getattr(_thread_local, "request_id", "-")
        record.user_id = getattr(_thread_local, "user_id", "-")
        return True
