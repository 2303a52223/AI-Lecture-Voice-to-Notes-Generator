"""
Centralized error handling utilities.
Logs detailed tracebacks and displays friendly messages to users.
"""
import traceback
import uuid
import time
import json
from datetime import datetime
from pathlib import Path


def _ensure_log_dir():
    logs_dir = Path(__file__).parent.parent / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def report_error(exc: Exception, context: str = None, user_facing: bool = True):
    """
    Log the exception with traceback and return/display a friendly message.

    Args:
        exc: The exception instance
        context: Optional context message describing where the error happened
        user_facing: If True, show a Streamlit-friendly error (imports Streamlit lazily)

    Returns:
        dict: {"id": uuid, "message": friendly_message}
    """
    err_id = uuid.uuid4().hex[:8]
    ts = datetime.utcnow().isoformat() + 'Z'
    logs_dir = _ensure_log_dir()
    log_path = logs_dir / 'errors.log'

    tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    log_entry = {
        'id': err_id,
        'timestamp': ts,
        'context': context or '',
        'traceback': tb,
        'message': str(exc),
    }

    try:
        # Append as JSON line for easier parsing
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception:
        # Swallow file logging errors to avoid cascading failures
        pass

    friendly = f"An unexpected error occurred. Reference ID: {err_id}."
    if context:
        friendly = f"{context}: {friendly}"

    if user_facing:
        try:
            import streamlit as st
            st.error(friendly)
            with st.expander("Show error details (for debugging)"):
                st.code(tb)
        except Exception:
            # If Streamlit isn't available, just print the message
            print(friendly)

    return {"id": err_id, "message": friendly}


def get_recent_errors(limit: int = 20):
    """Return the most recent error log entries (parsed JSON lines).

    Args:
        limit: Max number of entries to return (most recent first)

    Returns:
        list[dict]: List of parsed error objects
    """
    logs_dir = _ensure_log_dir()
    log_path = logs_dir / 'errors.log'
    if not log_path.exists():
        return []

    entries = []
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    # Fallback for legacy non-json lines: skip
                    continue
                entries.append(obj)
    except Exception:
        return []

    # Return most recent first
    entries.sort(key=lambda e: e.get('timestamp', ''), reverse=True)
    return entries[:limit]
