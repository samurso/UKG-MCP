"""Controlled task registry for SimTheory agent requests.

This module intentionally exposes only approved task names. It should not execute
arbitrary user-provided code or dynamically import functions based on a request.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, Optional

from .auth import get_access_token

TaskParameters = Optional[Dict[str, Any]]
TaskResult = Dict[str, Any]
TaskFunction = Callable[[TaskParameters], TaskResult]


def _is_configured(*environment_variable_names: str) -> bool:
    """Return True only when all provided environment variables are populated."""
    return all(bool(os.getenv(name)) for name in environment_variable_names)


def service_status(parameters: TaskParameters = None) -> TaskResult:
    """Return broad service readiness information without exposing secrets."""
    return {
        "success": True,
        "status": "ready",
        "service": "UKG-MCP SimTheory Bridge",
        "ukg_auth_configured": _is_configured(
            "UKG_TOKEN_URL",
            "UKG_CLIENT_ID",
            "UKG_CLIENT_SECRET",
        ),
        "available_tasks": [
            {
                "task": "service_status",
                "status": "available",
                "description": "Returns MCP bridge readiness and available task information.",
            },
            {
                "task": "test_authentication",
                "status": "available",
                "description": "Tests UKG authentication without returning the access token.",
            },
            {
                "task": "get_employee_names",
                "status": "blocked",
                "description": "Pending confirmation of the correct UKG employee endpoint path.",
            },
            {
                "task": "get_punches_by_date",
                "status": "blocked",
                "description": "Pending confirmation of the correct UKG punch/timekeeping endpoint path.",
            },
        ],
    }


def test_authentication(parameters: TaskParameters = None) -> TaskResult:
    """Validate UKG authentication while never returning the access token."""
    try:
        access_token = get_access_token()
        return {
            "success": True,
            "authenticated": bool(access_token),
            "message": "UKG authentication successful.",
        }
    except Exception as exc:
        return {
            "success": False,
            "authenticated": False,
            "message": "UKG authentication failed.",
            "error": str(exc),
        }


def get_employee_names_placeholder(parameters: TaskParameters = None) -> TaskResult:
    """Placeholder until the correct UKG employee endpoint is confirmed."""
    return {
        "success": False,
        "status": "blocked",
        "task": "get_employee_names",
        "message": (
            "UKG authentication works, but the exact employee endpoint path has "
            "not been confirmed yet. The initial /employees path returned 404."
        ),
        "next_step": "Confirm the correct UKG employee endpoint, parameters, and scopes.",
    }


def get_punches_by_date_placeholder(parameters: TaskParameters = None) -> TaskResult:
    """Define the SimTheory contract for future punch retrieval by date.

    This task is intentionally blocked from live UKG retrieval until the exact
    UKG punch/timekeeping endpoint, parameters, scopes, and response structure
    are confirmed by UKG documentation or an administrator.
    """
    parameters = parameters or {}
    requested_date = parameters.get("date")

    expected_parameters = {
        "date": "Required. Punch date in YYYY-MM-DD format.",
    }
    expected_output = [
        {
            "employee_id": "string",
            "employee_name": "string",
            "punch_date": "YYYY-MM-DD",
            "punch_in_time": "HH:MM or ISO-8601 timestamp",
            "punch_out_time": "HH:MM or ISO-8601 timestamp",
        }
    ]

    if not requested_date:
        return {
            "success": False,
            "status": "validation_error",
            "task": "get_punches_by_date",
            "message": "Missing required parameter: date.",
            "expected_parameters": expected_parameters,
            "example_request": {
                "task": "get_punches_by_date",
                "parameters": {
                    "date": "2026-05-22",
                },
            },
            "expected_output": expected_output,
        }

    return {
        "success": False,
        "status": "blocked_pending_ukg_endpoint",
        "task": "get_punches_by_date",
        "requested_date": requested_date,
        "message": (
            "The SimTheory bridge accepts this task contract, but live UKG punch "
            "retrieval is not enabled until the exact UKG punch/timekeeping "
            "endpoint path is confirmed."
        ),
        "expected_parameters": expected_parameters,
        "expected_output": expected_output,
        "next_step": (
            "Confirm the UKG punch endpoint path, required query/body parameters, "
            "required scopes or permissions, timezone handling, pagination rules, "
            "and sample response shape."
        ),
    }

TASK_REGISTRY: Dict[str, TaskFunction] = {
    "service_status": service_status,
    "test_authentication": test_authentication,
    "get_employee_names": get_employee_names_placeholder,
    "get_punches_by_date": get_punches_by_date_placeholder,
}


def execute_agent_task(task_name: str, parameters: TaskParameters = None) -> TaskResult:
    """Execute only a whitelisted task from the controlled registry."""
    normalized_task_name = (task_name or "").strip()

    if not normalized_task_name:
        return {
            "success": False,
            "error": "A task name is required.",
            "available_tasks": sorted(TASK_REGISTRY.keys()),
        }

    task_function = TASK_REGISTRY.get(normalized_task_name)
    if task_function is None:
        return {
            "success": False,
            "error": f"Unknown or unauthorized task: {normalized_task_name}",
            "available_tasks": sorted(TASK_REGISTRY.keys()),
        }

    result = task_function(parameters or {})
    return {
        "success": bool(result.get("success")),
        "task": normalized_task_name,
        "data": result,
    }
