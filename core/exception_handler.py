from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status


def flatten_errors(data) -> str:
    """Recursively flatten DRF error structures into a single human-readable string."""
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        parts = []
        for item in data:
            parts.append(flatten_errors(item))
        return " ".join(filter(None, parts))
    if isinstance(data, dict):
        # Prioritise 'detail' key first (most DRF errors)
        if "detail" in data:
            return flatten_errors(data["detail"])
        parts = []
        for key, value in data.items():
            msg = flatten_errors(value)
            if msg:
                parts.append(msg)
        return " ".join(parts)
    return str(data) if data else ""


def custom_exception_handler(exc, context):
    """
    Returns a flat JSON structure:
      { "status": 400, "message": "User with this email already exists." }
    instead of DRF's nested dict/list format.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        # Unhandled exception — let Django handle it (500 page)
        return response

    raw = response.data
    message = flatten_errors(raw).strip()

    # Clean up common unhelpful defaults
    if not message or message.lower() in ("", "null", "none"):
        message = "An unexpected error occurred. Please try again."

    response.data = {
        "status": response.status_code,
        "message": message,
    }

    return response