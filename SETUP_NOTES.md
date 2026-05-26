# UKG-MCP Local Setup Notes

This folder was created by Spark via Simlink as the local workspace for the UKG-MCP project.

Current local machine status:
- Git is not installed.
- System-wide Python is not installed.
- Windows Package Manager (`winget`) is not available.
- PowerShell is available.
- PowerShell `Expand-Archive` is available and was used to extract the manually downloaded GitHub ZIP.
- Portable Python has been installed inside `_tools/python-3.12.3-embed-amd64` and can run the project without a system-wide Python install.

Current project status:
- The GitHub repository files have been extracted into this local workspace.
- The local `.env` file has been created and populated with UKG production credentials and URLs.
- `.gitignore` includes `.env`, so local credentials should not be committed to GitHub.
- UKG authentication using OAuth Client Credentials Grant has succeeded.
- The initial `/employees` UKG path returned 404, so exact UKG data endpoint discovery is still pending.
- A FastAPI bridge has been added so SimTheory can call approved UKG-MCP tasks through protected API endpoints.

FastAPI bridge endpoints:
- `GET /health` is public and confirms the service is running.
- `GET /ukg/auth/test` is protected by `X-API-Key` and tests UKG authentication without returning the access token.
- `POST /agent/tasks` is protected by `X-API-Key` and executes only approved task names from the controlled registry.

Local run command from the `UKG-MCP` folder:

```powershell
$env:PYTHONPATH = (Get-Location).Path
.\_tools\python-3.12.3-embed-amd64\python.exe -m uvicorn ukg_mcp.api:app --host 127.0.0.1 --port 8000
```

Security note:
- API credentials should be stored only in the local `.env` file or secure deployment environment variables and never committed to GitHub.
- The SimTheory-facing API key is separate from UKG credentials and should be stored in `SIMTHEORY_API_KEY`.
- The API must never return the UKG access token to callers.

## 2026-05-22 Railway Deployment Preparation

Railway deployment preparation is now in place for the FastAPI bridge. Railway secrets must be configured in the Railway dashboard using environment variables, not committed to GitHub. Live UKG endpoint-specific data tasks remain pending until UKG confirms the required endpoint paths, parameters, scopes, and response formats.
