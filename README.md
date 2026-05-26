# UKG-MCP

## Overview
The UKG-MCP repository serves as the secure integration layer between UKG Pro and internal AI-enabled tools and reporting systems at Bolthouse Fresh Foods.

Its purpose is to enable structured, secure, and governed access to HR, Payroll, and Workforce data for automation, analytics, and operational efficiency.

---

## Business Objective
Support HR, Payroll, Benefits, and Workforce operations by:

- Enabling secure API access to UKG Pro data
- Supporting AI-driven insights and reporting
- Reducing manual reporting processes
- Improving data consistency across systems

---

## Initial Data Scope (Phase 1)

- Employee Master Data
- Job & Position Data
- Payroll Summary Data
- Accrual & Leave Balances

Future phases may include:
- Benefits data
- Organizational hierarchy
- Workforce planning metrics

---

## High-Level Architecture

UKG Pro API  
→ Secure MCP Layer  
→ Internal AI Tools / Data Warehouse / Reporting Systems  

---

## SimTheory Agent Bridge

The project now includes a FastAPI bridge so a SimTheory agent can call approved UKG-MCP tasks through secure HTTP endpoints. SimTheory should not receive or store UKG credentials directly. Instead, it calls the MCP API, and the MCP handles UKG authentication and task execution.

Initial endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Public service health check. |
| `GET` | `/ukg/auth/test` | Protected UKG authentication test that does not expose the access token. |
| `POST` | `/agent/tasks` | Protected endpoint for running approved SimTheory task names with optional parameters. |

Protected endpoints require an `X-API-Key` header matching the `SIMTHEORY_API_KEY` environment variable.

Example task request:

```json
{
  "task": "service_status",
  "parameters": {}
}
```

The first available tasks are `service_status` and `test_authentication`. UKG data retrieval tasks such as `get_employee_names` and `get_punches_by_date` are intentionally blocked until the correct UKG endpoint paths, parameters, scopes, and response shapes are confirmed.

---

## Local API Run Command

From the project root, run the FastAPI bridge with the portable Python runtime:

```powershell
$env:PYTHONPATH = (Get-Location).Path
.\_tools\python-3.12.3-embed-amd64\python.exe -m uvicorn ukg_mcp.api:app --host 127.0.0.1 --port 8000
```

Then test:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

---

## Railway Deployment Preparation

This project is prepared to deploy as a Railway-hosted FastAPI service connected to the GitHub repository.

Railway should use the deployment configuration in `railway.json`.

| Item | Value |
|---|---|
| App entrypoint | `ukg_mcp.api:app` |
| Start command | `uvicorn ukg_mcp.api:app --host 0.0.0.0 --port $PORT` |
| Health check path | `/health` |
| Protected task endpoint | `POST /agent/tasks` |

Required Railway environment variables for the current bridge are:

| Variable | Purpose |
|---|---|
| `UKG_TOKEN_URL` | UKG OAuth token endpoint. |
| `UKG_CLIENT_ID` | UKG production client ID. |
| `UKG_CLIENT_SECRET` | UKG client secret. |
| `SIMTHEORY_API_KEY` | API key required by protected SimTheory-facing endpoints. |

Future task-specific variables already documented in `.env.example` include `UKG_BASE_URL`, `UKG_APP_KEY`, `UKG_USERNAME`, and `UKG_PASSWORD`. These should only be populated in Railway if a future UKG task requires them.

After deployment, the public health check should be tested at:

```text
https://<railway-domain>/health
```

A protected task request can be tested with:

```http
POST https://<railway-domain>/agent/tasks
X-API-Key: <SIMTHEORY_API_KEY>
Content-Type: application/json
```

```json
{
  "task": "service_status",
  "parameters": {}
}
```

Never commit `.env` files or real secrets to GitHub. Configure production values only in the Railway dashboard or other approved secret-management system.

---

## Security & Governance

- OAuth 2.0 Authentication
- UKG credentials stored only in local `.env` or secure deployment environment variables
- SimTheory-facing endpoints protected by `SIMTHEORY_API_KEY`
- Controlled task registry prevents arbitrary code execution
- Role-based data access
- Data minimization principles
- Audit logging
- Compliance with internal data security policies

---

## Ownership

Business Owner: HR (Director, HRIS / Payroll / Benefits)  
Technical Owner: IT / Engineering  

---

## Status

Project initiated: May 2026  
Current Phase: Local API bridge development and UKG endpoint discovery
