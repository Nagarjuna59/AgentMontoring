# Ollama Setup and Troubleshooting Guide

## Quick Setup

### 1. Install Ollama
- **Windows**: Download from https://ollama.ai/download
- **Mac/Linux**: Run `curl -fsSL https://ollama.ai/install.sh | sh`

### 2. Start Ollama
```bash
ollama serve
```

### 3. Install the Required Model
```bash
ollama pull qwen2.5-coder:3b
```

### 4. Test Ollama
Run the health check script:
```bash
cd backend
python check_ollama.py
```

Or on Windows, double-click: `backend/test_ollama.bat`

---

## Troubleshooting

### Error: "Cannot connect to Ollama"

**Problem**: Ollama is not running

**Solutions**:
1. **Start Ollama manually**:
   ```bash
   ollama serve
   ```
   Leave this terminal window open

2. **Or start Ollama app**:
   - Windows: Search for "Ollama" in Start menu and run it
   - Mac: Open Ollama from Applications
   - Linux: Run `systemctl start ollama` (if installed as service)

3. **Verify Ollama is running**:
   - Open browser: http://localhost:11434
   - Should see: "Ollama is running"

---

### Error: "Model not found"

**Problem**: The model `qwen2.5-coder:3b` is not installed

**Solution**:
```bash
ollama pull qwen2.5-coder:3b
```

Wait for download to complete (may take a few minutes depending on internet speed)

**Verify installed models**:
```bash
ollama list
```

---

### Error: "Generation failed - please retry"

**Possible causes**:
1. Ollama stopped running
2. Model was not installed
3. Firewall blocking localhost:11434
4. Wrong model name in .env file

**Debug steps**:
1. Check if Ollama is running: http://localhost:11434
2. Run health check: `python backend/check_ollama.py`
3. Check backend logs for detailed error messages
4. Verify `.env` configuration:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   LLAMA_MODEL=qwen2.5-coder:3b
   ```

---

## Alternative: Use Groq API (Cloud)

If you can't run Ollama locally, use Groq's free API:

### 1. Get API Key
- Visit: https://console.groq.com/
- Sign up for free account
- Copy your API key

### 2. Update .env
```bash
# backend/.env
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=mixtral-8x7b-32768
LLM_FALLBACK_ENABLED=true
```

### 3. Restart Backend
```bash
cd backend
python app.py
```

---

## Configuration Options

### backend/.env
```bash
# Option 1: Use Ollama (Local, Free, Private)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
LLAMA_MODEL=qwen2.5-coder:3b
OLLAMA_TIMEOUT=120
OLLAMA_RETRIES=2

# Option 2: Use Groq (Cloud, Free Tier, Fast)
LLM_PROVIDER=groq
GROQ_API_KEY=your_key_here
GROQ_MODEL=mixtral-8x7b-32768
GROQ_TIMEOUT=90

# Fallback (if primary fails, try other provider)
LLM_FALLBACK_ENABLED=true
```

---

## Recommended Models

### Ollama Models (sorted by size)
- `qwen2.5-coder:3b` - **Recommended** (1.9GB, fast, good quality)
- `deepseek-coder:6.7b` - Better quality (3.8GB)
- `codellama:7b` - Meta's code model (3.8GB)
- `qwen2.5-coder:7b` - Best balance (4.7GB)

Install any model:
```bash
ollama pull <model-name>
```

Then update `.env`:
```bash
LLAMA_MODEL=<model-name>
```

---

## Performance Tips

### Fast Generation
- Use smaller model: `qwen2.5-coder:3b`
- Reduce timeout: `OLLAMA_TIMEOUT=60`

### Better Quality
- Use larger model: `qwen2.5-coder:7b`
- Increase retries: `OLLAMA_RETRIES=3`

### Hybrid Approach
- Primary: `LLM_PROVIDER=groq` (fast cloud API)
- Fallback: `LLM_FALLBACK_ENABLED=true` (local Ollama backup)

---

## Common Issues

### Issue: Response is too slow
**Solution**: Use smaller model or switch to Groq API

### Issue: Out of memory
**Solution**: Use `qwen2.5-coder:3b` (only 1.9GB RAM needed)

### Issue: Model keeps downloading on every request
**Solution**: Make sure `ollama pull` completed successfully

### Issue: Connection refused
**Solution**: Start Ollama server: `ollama serve`

---

## Getting Help

1. Check backend logs: Look for `[OLLAMA]` or `[GROQ]` messages
2. Run health check: `python backend/check_ollama.py`
3. Test Ollama directly:
   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "qwen2.5-coder:3b",
     "prompt": "Write hello world in Python",
     "stream": false
   }'
   ```

---

## Summary

✅ **For local/offline use**: Use Ollama  
✅ **For cloud/fast use**: Use Groq API  
✅ **For reliability**: Enable fallback mode  

**Recommended setup**:
```bash
LLM_PROVIDER=ollama
LLM_FALLBACK_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
LLAMA_MODEL=qwen2.5-coder:3b
```

**Start backend**:
```bash
cd backend
python app.py
```
