# AgentMonitor

Research-grounded Multi-Agent System (MAS) monitoring and code-generation platform with predictive scoring, benchmark evaluation, and production web UI.

## What This Project Implements

AgentMonitor follows the paper direction from `AgentMonitor.pdf`:
- Non-invasive monitoring of MAS execution.
- Behavioral indicator extraction from agent interactions.
- Quality prediction via XGBoost.
- Evaluation on representative tasks (code, reasoning, math).
- Security/safety awareness through observed behavior and judge-style scoring.

The current codebase extends the research approach with a full-stack product:
- FastAPI backend + MongoDB persistence.
- React frontend for user/admin workflows.
- Initial + enhanced generation workflow.
- Model-based score prediction with runtime monitor data.

## Architecture

- Frontend: `frontend/` (React)
- Backend API: `backend/app.py` (FastAPI)
- Core MAS + monitor: `AgentMonitor/`
- Training + verification scripts: `AgentMonitor/scripts/`
- Benchmarks: `AgentMonitor/BenchmarkDatasetFolder/`

### Runtime Flow
1. User submits a coding task from frontend.
2. Backend starts MAS generation.
3. Monitor captures agent stats, loops, latency, token usage, and graph edges.
4. Features are extracted and scored.
5. XGBoost predicts quality score.
6. Run data is stored and rendered in dashboard views.

## LLM Provider Strategy (Gemini + Ollama Fallback)

Primary provider: Gemini.
Fallback provider: Ollama (`qwen2.5-coder:3b`) for local resilience.

Implemented behavior:
- Backend uses a resilient LLM callable.
- If Gemini returns an error-like response (rate limit, API exhaustion, request failures), request is retried through Ollama automatically.
- Fallback is enabled by environment toggle.

### Required Environment Variables

Backend / LLM:
- `GEMINI_API_KEY_1` (required for Gemini primary)
- `GEMINI_API_KEY_2` (optional)
- `GEMINI_API_KEY_3` (optional)
- `LLM_PROVIDER` (`gemini` or `ollama`, default `gemini`)
- `LLM_FALLBACK_ENABLED` (`true` or `false`, default `true`)
- `OLLAMA_BASE_URL` (default `http://localhost:11434`)
- `LLAMA_MODEL` (default `qwen2.5-coder:3b`)
- `OLLAMA_TIMEOUT` (default `120`)

Backend / app:
- `MONGO_URI`
- `DB_NAME`
- `SECRET_KEY`
- `CORS_ORIGINS`

Frontend:
- `REACT_APP_API_URL` (default `http://localhost:8080/api`)

## API Endpoints Required by Frontend

Auth:
- `POST /api/login`
- `POST /api/register`

Generation:
- `POST /api/run-mas`
- `POST /api/run-mas-start`
- `GET /api/run/{run_id}`

User/Admin data:
- `GET /api/runs/user`
- `GET /api/runs/all`
- `GET /api/graph-metrics/{run_id}`
- `GET /api/dashboard-summary`
- `GET /api/export_csv`

## Frontend Upgrades Added

- Global LeetCode-style skills theme selector across all pages.
- Persistent theme preference in `localStorage`.
- Shared token-based styling via CSS variables.
- API client timeout and environment-driven base URL.
- Registration flow unified through shared API client.

Theme options:
- `LeetCode`
- `Focus`
- `Classic`

## Research-Based Feature Expansion Roadmap

### Extra Features to Add Next
1. Early-exit predictor: stop MAS when confidence crosses threshold.
2. Per-agent reliability index: combine score variance, latency stability, retry pressure.
3. Provider telemetry: fallback counters, provider latency histograms, outage windows.
4. Security signal layer: detect suspicious prompt trajectories and risky tool intent.
5. Difficulty-aware orchestration: map task complexity to agent topology automatically.

### Improve Existing Features
1. Harden fallback with explicit failure taxonomy and circuit breaker.
2. Unify LLM call path across backend and monitor for consistent behavior.
3. Improve monitor data schema versioning for long-term analytics compatibility.
4. Add dashboard performance optimization for large run histories.
5. Add end-to-end tests for fallback and enhancement polling.

## Local Run

Backend:
```powershell
cd backend
python app.py
```

Frontend:
```powershell
cd frontend
npm install
npm start
```

## Ollama Local Setup (qwen2.5-coder:3b)

```powershell
ollama pull qwen2.5-coder:3b
ollama serve
```

Then set:
- `LLM_PROVIDER=gemini`
- `LLM_FALLBACK_ENABLED=true`
- `OLLAMA_BASE_URL=http://localhost:11434`
- `LLAMA_MODEL=qwen2.5-coder:3b`

## Current Status

- Documentation reset complete (single README + MEMORY).
- Backend fallback path integrated.
- Theme system integrated globally.
- Frontend API client improved for deployability.
