"""FastAPI bridge exposing approved UKG-MCP tasks to SimTheory."""

from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from .agent_tasks import execute_agent_task, test_authentication

load_dotenv()

app = FastAPI(
    title="UKG-MCP SimTheory Bridge",
    description="Secure API bridge for approved SimTheory requests into UKG-MCP.",
    version="0.1.0",
)


class AgentTaskRequest(BaseModel):
    """Request model for controlled SimTheory task execution."""

    task: str = Field(..., description="Approved task name to execute.")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="Task-specific parameters. Only approved tasks are executed.",
    )


def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    """Validate the SimTheory API key before protected operations."""
    expected_api_key = os.getenv("SIMTHEORY_API_KEY")

    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail="SIMTHEORY_API_KEY is not configured for protected endpoints.",
        )

    if not x_api_key or x_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Public health check for uptime monitoring."""
    return {
        "status": "ok",
        "service": "UKG-MCP SimTheory Bridge",
    }


@app.get("/ukg/auth/test")
def ukg_auth_test(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> Dict[str, Any]:
    """Protected endpoint to test UKG authentication without exposing tokens."""
    verify_api_key(x_api_key)
    result = test_authentication({})
    return {
        "success": bool(result.get("success")),
        "data": result,
    }


@app.post("/agent/tasks")
def run_agent_task(
    request: AgentTaskRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> Dict[str, Any]:
    """Run a controlled task requested by SimTheory."""
    verify_api_key(x_api_key)
    return execute_agent_task(request.task, request.parameters)
