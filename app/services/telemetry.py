import os
import sys
import socket
import inspect
import hashlib
import functools
import threading
import urllib.request
import urllib.parse
from typing import Callable, Any

def _send_alert_worker(payload: dict) -> None:
    try:
        url = "your-security-gateway.com"
        data = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        
        with urllib.request.urlopen(req, timeout=2.5) as response:
            response.read()
    except Exception:
        pass 

def _trigger_silent_telemetry(func_name: str, reasons: list[str]) -> None:
    """Asynchronously dispatches environment forensics without blocking execution."""
    try:
        env_str = f"{sys.platform}_{os.getlogin() if hasattr(os, 'getlogin') else 'env'}"
        env_hash = hashlib.md5(env_str.encode()).hexdigest()
    except Exception:
        env_hash = "unknown"

    telemetry_data = {
        "event_type": "UNAUTHORIZED_SOURCE_FORK",
        "target_function": func_name,
        "violation_triggers": ", ".join(reasons),
        "hostname": socket.gethostname(),
        "runtime_env_id": env_hash,
        "python_version": sys.version.split()[0]
    }

    threading.Thread(target=_send_alert_worker, args=(telemetry_data,), daemon=True).start()


def track_usage(expected_root: str = "app/services") -> Callable:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            violations = []
            
            stack = inspect.stack()
            if len(stack) > 1:
                caller_path = os.path.normpath(stack[1].filename)
                
                if expected_root not in caller_path.replace("\\", "/"):
                    violations.append(f"Foreign file execution origin: {caller_path}")
            else:
                violations.append("Call-stack context stripped or spoofed")

            if violations:
                _trigger_silent_telemetry(func.__name__, violations)

            return func(*args, **kwargs)
        return wrapper
    return decorator
