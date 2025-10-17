---
title: My TDS Project
emoji: 🧮
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "3.39.0"
app_file: app.py
pinned: false
---
# Deploying to Hugging Face Spaces (static Python space)

This project can be hosted on Hugging Face Spaces as a simple Python web app.

Required steps:

1. Create a new Space (type: "Gradio or Static" -> choose "Other" or "Gradio" for Python support).
2. Upload the repo contents or connect your GitHub repo to the Space.
3. Ensure the following files are present at the repo root in the Space:
   - `app.py` (entrypoint) — included in this repo.
   - `requirements.txt` — included.
   - `.env` — set as secrets in the Space settings (do NOT upload `.env` to the repo). Set `GITHUB_TOKEN`, `secret`, and optionally `OPENAI_API_KEY`.

Port
- The app listens on `PORT` environment variable; Spaces sets a port automatically.

Notes
- Use Secrets in Space settings to set `GITHUB_TOKEN` and `OPENAI_API_KEY`.
- Avoid storing secrets in the repo.
## Docker support

If you prefer to deploy using a Docker image (Hugging Face Spaces supports Docker-backed Spaces), this repo includes a `Dockerfile` at the project root.

Build locally:

```powershell
docker build -t tds-project:latest .
docker run --rm -p 7860:7860 -e GITHUB_TOKEN="$env:GITHUB_TOKEN" -e secret="$env:secret" tds-project:latest
```

Replace the environment vars with your secrets or pass them in the Space using the Secrets UI.

Deploy to a Docker-backed Space:

1. Create a new Space and choose the Docker option (if available) or connect your GitHub repo and add a `Dockerfile`. Spaces will build the Docker image from your `Dockerfile`.
2. In Space settings, add the Secrets (`GITHUB_TOKEN`, `secret`, `OPENAI_API_KEY` as needed).
3. Start the Space. The container will run `python app.py` which binds to `$PORT`.

Notes:
- The provided `Dockerfile` uses a Debian-slim base, installs `git`, and installs packages from `requirements.txt`.
- If you want to run the FastAPI app with UVicorn in the container instead, change the `CMD` to:

```dockerfile
CMD ["uvicorn", "src.fastapi_app:app", "--host", "0.0.0.0", "--port", "7860"]
```

or pass a start command through Hugging Face Space settings using `$PORT`.
