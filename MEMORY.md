# MEMORY

Operational memory for the AgentMonitor repository.

## Ground Truth

- Core research reference is `AgentMonitor.pdf` (29 pages).
- Project scope is MAS monitoring + predictive quality scoring + full-stack productization.
- Web stack: FastAPI backend, React frontend, MongoDB storage.
- Predictor: XGBoost model loaded from `AgentMonitor/models/mas_predictor.pkl` when available.

## Key Engineering Decisions

1. Markdown reset policy:
- All legacy markdown files were removed.
- Only root `README.md` and root `MEMORY.md` are maintained.

2. LLM provider policy:
- Primary provider: Gemini.
- Automatic fallback: Ollama (`qwen2.5-coder:3b`) for Gemini failures.
- Fallback behavior controlled through env vars.

3. Frontend UX policy:
- Global LeetCode-style skills theme selector is available on all routes.
- Theme state persists in `localStorage` via `skillTheme` key.

## Important Files

Backend:
- `backend/app.py` (provider routing, API entrypoints, fallback usage)

Frontend:
- `frontend/src/context/ThemeContext.js`
- `frontend/src/components/ThemeSelector.js`
- `frontend/src/components/ThemeSelector.css`
- `frontend/src/index.css`
- `frontend/src/App.js`
- `frontend/src/api.js`

## Environment Contracts

Required:
- `MONGO_URI`
- `DB_NAME`
- `SECRET_KEY`
- `GEMINI_API_KEY_1`

Optional/Recommended:
- `GEMINI_API_KEY_2`
- `GEMINI_API_KEY_3`
- `LLM_PROVIDER` (`gemini`/`ollama`)
- `LLM_FALLBACK_ENABLED` (`true`/`false`)
- `OLLAMA_BASE_URL`
- `LLAMA_MODEL` (default `qwen2.5-coder:3b`)
- `OLLAMA_TIMEOUT`
- `REACT_APP_API_URL`

## Known Risks

1. Fallback detection currently relies on error-string heuristics from provider wrappers.
2. Some older CSS files still use static colors and should be gradually tokenized.
3. Large historical run lists may need pagination/virtualization in admin analytics.

## Next High-Value Improvements

1. Replace error-string fallback detection with typed exceptions in LLM wrappers.
2. Add provider health endpoint and fallback counters for observability.
3. Add tests for:
- Gemini failure -> Ollama success path.
- run-mas-start polling completion.
- Theme persistence across route changes and reload.
4. Add structured benchmark experiment logging for reproducibility.

## Minimal Maintenance Checklist

Per release:
1. Validate backend startup and model loading logs.
2. Validate login/register/run flow from frontend.
3. Simulate Gemini failure and verify Ollama fallback.
4. Verify theme selector behavior on home, login, register, user, and admin pages.
