# LLM Code Deployment - Student Service

This project implements the student-side service for the LLM Code Deployment assignment.

Overview
- A Flask API accepts task POST requests (JSON) at `/api-endpoint`.
- It verifies a shared secret, generates a minimal app from the brief and attachments, creates a GitHub repo, enables Pages, and notifies the instructor evaluation URL.

See `src/` for the code.

Environment
- Python 3.10+
- Environment variables:
  - `GITHUB_TOKEN` - Personal access token with repo and pages scopes.
- `GITHUB_TOKEN` - Personal access token with repo and pages scopes.
- `secret` - The secret students registered in the form (the server reads `secret` env var; `SHARED_SECRET` is also supported as a fallback).
- `GITHUB_OWNER` - Optional: GitHub username/organization to create repos under (default: authenticated user).
- `OPENAI_API_KEY` - Optional: provide to enable LLM-assisted generation.

Quick start

1. Create a virtualenv and install dependencies:

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the server:

```pwsh
$. .\scripts\set-env.ps1   # dot-source to load values from .env or set manually as below
$env:secret='mysecret'
$env:GITHUB_TOKEN='ghp_...'
#$env:OPENAI_API_KEY='sk_...'
python -m src.server
```

3. Example curl to test:

```pwsh
curl http://localhost:5000/api-endpoint -H "Content-Type: application/json" -d '{"email":"student@example.com","secret":"mysecret","task":"demo-1","round":1,"nonce":"n1","brief":"Publish a page that shows Hello","checks":[],"evaluation_url":"http://localhost:9000/eval","attachments":[]}'
```

Notes and security
- Do not commit tokens to git. The server avoids writing secrets into the repo history.
- This scaffold uses a simple generator (no external LLM); replace `generator.generate_app` with calls to your LLM of choice.

Hugging Face Spaces
- This project can be deployed to a Hugging Face Space. See `HF_DEPLOY.md` for details. Ensure you set `GITHUB_TOKEN`, `secret`, and `OPENAI_API_KEY` (optional) as Space Secrets.
- If `OPENAI_API_KEY` is provided, the service will call the OpenAI Chat Completions API to generate files. The generator falls back to a simple static page if the LLM key is not set or the call fails.
