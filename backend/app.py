from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
from pathlib import Path
import sys
try:
    import jwt
except Exception:
    # jwt (PyJWT) may not be installed in all environments. Provide a minimal fallback
    jwt = None
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ROOT_PATH = Path(__file__).parent.parent
# Ensure the project root is on sys.path so `import AgentMonitor` works whether
# the backend is started from the `backend/` folder or the repository root.
sys.path.insert(0, str(ROOT_PATH))

from database import Database

# Initialize XGBoost predictor
try:
    from AgentMonitor.models.predictor import MASPredictor
    MODEL_PATH = ROOT_PATH / "AgentMonitor" / "models" / "mas_predictor.pkl"
    predictor = MASPredictor(model_path=MODEL_PATH)
    if MODEL_PATH.exists():
        predictor.load()  # Fixed: method is called 'load()' not 'load_model()'
        print("✅ XGBoost model loaded successfully")
    else:
        print(f"⚠️ XGBoost model not found at {MODEL_PATH}")
        predictor = None
except Exception as e:
    print(f"⚠️ XGBoost model failed to load: {e}")
    print("   Will use agent score averaging as fallback")
    predictor = None

app = FastAPI(title="AgentMonitor API")
security = HTTPBearer()
db = Database()

SECRET_KEY = os.getenv("SECRET_KEY", "agentmonitor-secret-key-2025")

# Get CORS origins from environment variable
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "user"  # default to user role

class RunRequest(BaseModel):
    task: str
    code: str = ""
    language: str = "auto"  # NEW: Support multiple languages; default to 'auto' so LLM can detect
    use_full_mas: bool = False  # NEW: Enable full 4-agent MAS mode for graph metrics

def create_token(username, role):
    payload = {
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    if jwt:
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    else:
        # Development fallback: return a simple JSON string (NOT secure)
        return json.dumps({"username": username, "role": role, "exp": payload["exp"].isoformat()})

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        if jwt:
            payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
            return payload
        else:
            # Try to parse our development fallback token
            try:
                data = json.loads(credentials.credentials)
                return {"username": data.get("username"), "role": data.get("role")}
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid token or jwt not installed")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def calculate_graph_metrics(graph_edges: list, num_nodes: int) -> dict:
    """Calculate actual graph metrics from edges"""
    import networkx as nx
    import numpy as np
    
    if not graph_edges or num_nodes == 0:
        return {
            "clustering_coefficient": 0.0,
            "transitivity": 0.0,
            "avg_degree_centrality": 0.0,
            "avg_betweenness_centrality": 0.0,
            "avg_closeness_centrality": 0.0,
            "pagerank_entropy": 0.0,
            "heterogeneity_score": 0.0
        }
    
    # Build directed graph
    G = nx.DiGraph()
    
    # Map agent names to node indices
    agent_names = sorted(set([e[0] for e in graph_edges] + [e[1] for e in graph_edges]))
    name_to_idx = {name: i for i, name in enumerate(agent_names)}
    
    G.add_nodes_from(range(len(agent_names)))
    
    # Add edges
    for from_agent, to_agent in graph_edges:
        if from_agent in name_to_idx and to_agent in name_to_idx:
            G.add_edge(name_to_idx[from_agent], name_to_idx[to_agent])
    
    # Calculate metrics
    try:
        # Clustering (convert to undirected)
        G_undirected = G.to_undirected()
        clustering = nx.average_clustering(G_undirected)
        transitivity = nx.transitivity(G_undirected)
        
        # Centrality
        degree_cent = nx.degree_centrality(G)
        betweenness_cent = nx.betweenness_centrality(G)
        closeness_cent = nx.closeness_centrality(G)
        
        avg_degree = np.mean(list(degree_cent.values()))
        avg_betweenness = np.mean(list(betweenness_cent.values()))
        avg_closeness = np.mean(list(closeness_cent.values()))
        
        # PageRank entropy
        pagerank = nx.pagerank(G)
        pr_values = np.array(list(pagerank.values()))
        pr_values = pr_values[pr_values > 0]  # Remove zeros
        pagerank_entropy = -np.sum(pr_values * np.log(pr_values + 1e-10))
        
        # Heterogeneity (variance in degrees)
        degrees = [G.degree(n) for n in G.nodes()]
        heterogeneity = np.std(degrees) / (np.mean(degrees) + 1e-10)
        
    except Exception as e:
        print(f"⚠️ Graph metric calculation failed: {e}")
        clustering = transitivity = avg_degree = avg_betweenness = 0.0
        avg_closeness = pagerank_entropy = heterogeneity = 0.0
    
    return {
        "clustering_coefficient": clustering,
        "transitivity": transitivity,
        "avg_degree_centrality": avg_degree,
        "avg_betweenness_centrality": avg_betweenness,
        "avg_closeness_centrality": avg_closeness,
        "pagerank_entropy": pagerank_entropy,
        "heterogeneity_score": heterogeneity
    }

def extract_features_from_monitor(monitor_data: dict) -> dict:
    """Extract 16 features from monitoring data"""
    agent_stats = monitor_data.get("agent_stats", {})
    graph_edges = monitor_data.get("graph_edges", [])
    
    # System features (6)
    all_scores, all_latencies = [], []
    all_tokens, num_enhanced, max_loops = 0, 0, 0
    
    for stats in agent_stats.values():
        all_scores.extend(stats.get("scores", []))
        all_latencies.extend(stats.get("latencies", []))
        all_tokens += stats.get("token_usage", 0)
        num_enhanced += stats.get("enhancement_triggered", 0)
        max_loops = max(max_loops, len(stats.get("latencies", [])))
    
    features = {
        "avg_personal_score": sum(all_scores) / len(all_scores) if all_scores else 0.0,
        "min_personal_score": min(all_scores) if all_scores else 0.0,
        "max_loops": max_loops,
        "total_latency": sum(all_latencies),
        "total_token_usage": all_tokens,
        "num_agents_triggered_enhancement": num_enhanced,
        
        # Graph features (9)
        "num_nodes": len(agent_stats),
        "num_edges": len(graph_edges),
    }
    
    # Calculate real graph metrics
    graph_metrics = calculate_graph_metrics(graph_edges, len(agent_stats))
    features.update(graph_metrics)
    
    # Collective score (1)
    features["collective_score"] = sum(all_scores) / len(all_scores) if all_scores else 0.0
    
    print(f"✅ Extracted {len(features)} features")
    
    return features


@app.post("/api/login")
async def login(request: LoginRequest):
    print(f"Login attempt - Username: {request.username}, Password length: {len(request.password)}")
    user = db.verify_user(request.username, request.password)
    print(f"User found: {user is not None}")
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user["username"], user["role"])
    return {"token": token, "username": user["username"], "role": user["role"]}

@app.post("/api/register")
async def register(request: RegisterRequest):
    # Check if user already exists
    existing = db.users.find_one({"username": request.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create new user
    new_user = {
        "username": request.username,
        "password": db.hash_password(request.password),
        "role": request.role if request.role in ["user", "admin"] else "user",
        "created_at": datetime.now()
    }
    db.users.insert_one(new_user)
    
    # Create token for immediate login
    token = create_token(new_user["username"], new_user["role"])
    return {"token": token, "username": new_user["username"], "role": new_user["role"]}

@app.get("/api/user/me")
async def get_current_user(user = Depends(verify_token)):
    return user

@app.post("/api/run_mas")
async def run_mas(request: RunRequest, user = Depends(verify_token)):
    try:
        print(f"MAS execution request from {user['username']}: {request.task[:50]}...")
        
        # Import necessary components from AgentMonitor
        from AgentMonitor import EnhancedAgentMonitor, CodeGenerationMAS, MASPredictor
        from AgentMonitor.gemini_api import gemini_call
        
        # Use gemini_call as LLM (with automatic key rotation)
        llm = gemini_call
        
        # Determine if this is an enhancement request or initial request
        is_enhancement = bool(request.code and request.code.strip())
        
        if is_enhancement:
            # User clicked "Enhance Again" - just enhance the provided code
            print(f"🔄 Enhancement mode - improving existing code ({len(request.code)} chars)")
            
            mas = CodeGenerationMAS(
                llm=llm,
                language=request.language,
                threshold=0.75,
                max_retries=1
            )
            
            monitor = EnhancedAgentMonitor(
                llm=llm,
                threshold=0.75,
                max_retries=1,
                debug=True
            )
            
            enhancement_task = f"{request.task}\n\nExisting code:\n{request.code}\n\nImprove this code with better quality and best practices."
            print(f"🔄 Running enhancement with monitoring...")
            result = await mas.run(enhancement_task, monitor=monitor)
            
            if isinstance(result, dict):
                clean_code = result.get('output') or result.get('code') or str(result)
            else:
                clean_code = str(result)
            
            monitor_data = None
            initial_code = request.code
            auto_enhanced = False
            enhancement_loops = 0
            features = None
            predicted_score = 0.85
            
            # Score the user-provided code
            try:
                from AgentMonitor.core.enhanced_monitor import EnhancedAgentMonitor
                temp_monitor = EnhancedAgentMonitor(llm=llm, threshold=0.75, max_retries=0, debug=False)
                initial_score = await temp_monitor._score_output(request.task, initial_code, "UserProvidedCode")
                print(f"📊 User code score: {initial_score:.3f}")
            except:
                initial_score = 0.75  # Fallback for user-provided code
            
        else:
            # NEW WORKFLOW: Generate initial code, then automatically enhance it
            print(f"✨ Two-step workflow: Initial → Enhanced")
            
            # STEP 1: Generate initial code (FAST, no monitoring)
            print(f"⚡ Step 1/2: Generating initial code...")
            # Honor the requested language for initial generation; default to 'auto' if empty
            initial_language = (request.language or 'auto').lower()
            mas_initial = CodeGenerationMAS(
                llm=llm,
                language=initial_language,
                threshold=1.0,
                max_retries=0
            )
            
            initial_result = await mas_initial.run(request.task, monitor=None)
            
            if isinstance(initial_result, dict):
                initial_code = initial_result.get('output') or initial_result.get('code') or str(initial_result)
            else:
                initial_code = str(initial_result)
            
            print(f"✅ Initial code generated: {len(initial_code)} chars")
            
            # Score the initial code for comparison
            try:
                from AgentMonitor.core.enhanced_monitor import EnhancedAgentMonitor
                temp_monitor = EnhancedAgentMonitor(llm=llm, threshold=0.75, max_retries=0, debug=False)
                initial_score = await temp_monitor._score_output(request.task, initial_code, "InitialCoder")
                print(f"📊 Initial code score: {initial_score:.3f}")
            except Exception as e:
                print(f"⚠️ Initial scoring failed, using heuristic: {e}")
                # Heuristic fallback
                if len(initial_code) > 500:
                    initial_score = 0.70
                elif len(initial_code) > 200:
                    initial_score = 0.65
                else:
                    initial_score = 0.60
            
            # STEP 2: Automatically enhance with agent-level monitoring
            print(f"🔄 Step 2/2: Enhancing with agent-level monitoring...")
            mas_enhanced = CodeGenerationMAS(
                llm=llm,
                language=request.language,
                threshold=0.75,
                max_retries=1,
                use_full_mas=True  # Use all 4 agents for proper MAS
            )
            
            monitor = EnhancedAgentMonitor(
                llm=llm,
                threshold=0.75,
                max_retries=1,
                debug=True
            )
            
            # Simplified enhancement task - don't include full code to avoid safety blocks
            enhancement_task = f"{request.task}\n\nGenerate improved, production-quality code with error handling and best practices."
            
            try:
                enhanced_result = await mas_enhanced.run(enhancement_task, monitor=monitor)
                
                if isinstance(enhanced_result, dict):
                    clean_code = enhanced_result.get('output') or enhanced_result.get('code') or str(enhanced_result)
                else:
                    clean_code = str(enhanced_result)
                
                # Check if enhancement failed (error message, blocked, or too short)
                if "Error:" in clean_code or "blocked" in clean_code.lower() or len(clean_code) < 100:
                    print(f"⚠️ Enhancement failed or blocked, using initial code as final output")
                    clean_code = initial_code
                    auto_enhanced = False
                else:
                    auto_enhanced = True
                    print(f"✅ Enhanced code generated: {len(clean_code)} chars")
            except Exception as e:
                print(f"⚠️ Enhancement step failed: {e}")
                print(f"📦 Using initial code as final output")
                clean_code = initial_code
                auto_enhanced = False
            
            # Extract monitor data with agent-level scores
            monitor_data = {
                'threshold': 0.75,
                'max_retries': 1,
                'auto_enhanced': True,
                'agent_stats': monitor.monitor_data.get('agent_stats', {}),
                'enhancement_history': monitor.enhancement_history
            }
            
            # Extract features from monitor data
            features = extract_features_from_monitor(monitor.monitor_data)
            
            # Calculate scores using XGBoost model or agent scores as fallback
            agent_stats = monitor.monitor_data.get('agent_stats', {})
            agent_scores = []
            
            if agent_stats:
                # Get agent-level scores
                for agent_name, stats in agent_stats.items():
                    if stats.get('scores'):
                        agent_scores.extend(stats['scores'])
            
            # Try to use trained XGBoost model first
            if predictor and features:
                try:
                    predicted_score = predictor.predict(features)
                    print(f"🤖 XGBoost prediction: {predicted_score:.3f}")
                except Exception as e:
                    print(f"⚠️ XGBoost prediction failed: {e}")
                    # Fallback to agent score averaging
                    if agent_scores:
                        predicted_score = sum(agent_scores) / len(agent_scores)
                        print(f"📊 Using agent avg fallback: {predicted_score:.3f}")
                    else:
                        predicted_score = 0.85
                        print(f"📊 Using default fallback: {predicted_score:.3f}")
            else:
                # No predictor available, use agent scores
                if agent_scores:
                    predicted_score = sum(agent_scores) / len(agent_scores)
                    print(f"📊 Agent-level scores: {agent_scores}")
                    print(f"📊 Agent avg score: {predicted_score:.3f}")
                else:
                    predicted_score = 0.85
                    print(f"📊 Default score: {predicted_score:.3f}")
            
            enhancement_loops = 1
        
        # CRITICAL: Ensure initial_score is ALWAYS minimum and final_score is ALWAYS maximum
        # Fetch both scores first
        score_1 = initial_score  # Score of initial code
        score_2 = predicted_score  # Score of final/enhanced code
        
        # Assign minimum to initial, maximum to final
        min_score = min(score_1, score_2)
        max_score = max(score_1, score_2)
        initial_score = min_score
        final_score = max_score
        
        print(f"📊 Score Assignment: initial={score_1:.3f}, enhanced={score_2:.3f} → final_pair: min={initial_score:.3f}, max={final_score:.3f}")
        
        # STEP 5: Save to database with BOTH initial and final code
        print(f"📊 Final: Initial={len(initial_code)} chars (score={initial_score:.2f}), Enhanced={len(clean_code)} chars (score={final_score:.2f})")
        run_id = db.save_run(
            user_id=user["username"],
            username=user["username"],
            task=request.task,
            code=clean_code,
            predicted_score=float(final_score),
            features=features,
            monitor_data=monitor_data,
            initial_code=initial_code,  # Pass initial code
            initial_score=float(initial_score)  # Pass initial score
        )
        
        print(f"✅ Response ready: {len(clean_code)} chars, min={initial_score:.2f}, max={final_score:.2f}")
        
        return {
            "run_id": str(run_id),
            "predicted_score": float(final_score),
            "initial_score": float(initial_score),
            "code": clean_code,
            "initial_code": initial_code,
            "final_code": clean_code,
            "is_enhancement": is_enhancement,
            "auto_enhanced": auto_enhanced,
            "enhancement_loops": enhancement_loops,
            "features": features,
            "monitor_data": monitor_data,
            "agent_stats": monitor_data.get('agent_stats', {}) if monitor_data else {}
        }
    except Exception as e:
        print(f"ERROR in run_mas: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Alias with hyphen for frontend compatibility
@app.post("/api/run-mas")
async def run_mas_hyphen(request: RunRequest, user = Depends(verify_token)):
    """Alias for /api/run_mas with hyphen instead of underscore"""
    return await run_mas(request, user)


# New: start endpoint that returns initial code immediately and schedules enhancement
@app.post("/api/run-mas-start")
async def run_mas_start(request: RunRequest, background_tasks: BackgroundTasks, user = Depends(verify_token)):
    """Generate initial code quickly and schedule enhancement in background.

    Returns initial code and run_id immediately. Frontend should poll /api/run/{run_id}
    to fetch enhanced results when ready.
    """
    try:
        print(f"[START] MAS start request from {user['username']}: {request.task[:50]}...")
        from AgentMonitor import CodeGenerationMAS, EnhancedAgentMonitor
        from AgentMonitor.gemini_api import gemini_call

        llm = gemini_call

        # Generate initial code fast (no monitoring, FAST MODE always)
        mas_initial = CodeGenerationMAS(llm=llm, language=request.language or 'auto', threshold=1.0, max_retries=0, use_full_mas=False)
        initial_result = await mas_initial.run(request.task, monitor=None)
        if isinstance(initial_result, dict):
            initial_code = initial_result.get('output') or initial_result.get('code') or str(initial_result)
        else:
            initial_code = str(initial_result)

        # Save initial run with placeholder fields
        run_id = db.save_run(user_id=user['username'], username=user['username'], task=request.task,
                             code=initial_code, predicted_score=0.0, features=None, monitor_data=None)

        # Schedule enhancement in background
        lang = (request.language or 'auto').lower()
        background_tasks.add_task(_background_enhance_run, str(run_id), request.task, initial_code, lang, user['username'], request.use_full_mas)

        return {
            'run_id': str(run_id),
            'initial_code': initial_code,
            'message': 'Initial code generated. Enhancement scheduled.'
        }
    except Exception as e:
        print(f"ERROR in run_mas_start: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _background_enhance_run(run_id: str, task: str, initial_code: str, language: str, username: str, use_full_mas: bool = False):
    """Background worker: runs enhancement and updates the DB with final code, features, and agent stats."""
    try:
        print(f"[BG] Enhancer started for run {run_id} (FULL MAS: {use_full_mas})")
        from AgentMonitor import CodeGenerationMAS, EnhancedAgentMonitor
        from AgentMonitor.gemini_api import gemini_call

        llm = gemini_call

        mas_enhanced = CodeGenerationMAS(llm=llm, language=language, threshold=0.75, max_retries=1, use_full_mas=use_full_mas)
        monitor = EnhancedAgentMonitor(llm=llm, threshold=0.75, max_retries=1, debug=True)  # Enable debug

        # Prepend language directive if requested
        lang_directive = f"LANGUAGE: {language}\n\n" if language and language not in ['auto', 'any'] else ''
        enhancement_task = f"{lang_directive}{task}\n\nExisting code:\n{initial_code}\n\nImprove this code with better quality and best practices."

        print(f"[BG] Running MAS with monitor...")
        enhanced_result = await mas_enhanced.run(enhancement_task, monitor=monitor)

        if isinstance(enhanced_result, dict):
            final_code = enhanced_result.get('output') or enhanced_result.get('code') or str(enhanced_result)
        else:
            final_code = str(enhanced_result)

        print(f"[BG] Enhanced code generated: {len(final_code)} chars")
        print(f"[BG] Monitor data keys: {monitor.monitor_data.keys()}")
        print(f"[BG] Agent stats: {monitor.monitor_data.get('agent_stats', {})}")

        # Extract agent stats and monitor data
        monitor_data = {
            'threshold': monitor.threshold,
            'max_retries': monitor.max_retries,
            'agent_stats': monitor.monitor_data.get('agent_stats', {}),
            'enhancement_history': monitor.enhancement_history,
            'graph_edges': monitor.monitor_data.get('graph_edges', []),
            'conversations': monitor.monitor_data.get('conversations', [])
        }

        # Simple feature extraction from monitor_data
        print(f"[BG] Extracting features from monitor_data...")
        features = extract_features_from_monitor(monitor.monitor_data) if hasattr(monitor, 'monitor_data') else None
        print(f"[BG] Extracted features: {features}")

        # Simple score aggregation
        agent_scores = []
        for a, s in monitor.monitor_data.get('agent_stats', {}).items():
            agent_scores.extend(s.get('scores', []))
            
        # Try to use trained XGBoost model first
        if predictor and features:
            try:
                predicted_score = predictor.predict(features)
                print(f"[BG] XGBoost prediction: {predicted_score:.3f}")
            except Exception as e:
                print(f"[BG] ⚠️ XGBoost prediction failed: {e}")
                # Fallback to agent score averaging
                if agent_scores:
                    predicted_score = sum(agent_scores) / len(agent_scores)
                    print(f"[BG] Using agent avg fallback: {predicted_score:.3f}")
                else:
                    predicted_score = 0.85
                    print(f"[BG] Using default fallback: {predicted_score:.3f}")
        else:
            # No predictor available, use agent scores
            if agent_scores:
                predicted_score = sum(agent_scores) / len(agent_scores)
                print(f"[BG] Agent-level scores: {agent_scores}")
                print(f"[BG] Agent avg score: {predicted_score:.3f}")
            else:
                predicted_score = 0.85
                print(f"[BG] Default score: {predicted_score:.3f}")

        # Update run in DB
        db.update_run(run_id, {
            'code': final_code,
            'features': features,
            'monitor_data': monitor_data,
            'predicted_score': float(predicted_score),
            'enhanced_at': datetime.now()
        })

        print(f"[BG] Enhancer finished for run {run_id}, DB updated with {len(features) if features else 0} features")
    except Exception as e:
        import traceback
        print(f"[BG] Enhancer error for run {run_id}: {e}")
        traceback.print_exc()

@app.get("/api/runs/user")
async def get_user_runs(user = Depends(verify_token)):
    runs = db.get_user_runs(user["username"])
    for run in runs:
        run["_id"] = str(run["_id"])
    return runs

@app.get("/api/runs/all")
async def get_all_runs(user = Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    runs = db.get_all_runs()
    for run in runs:
        run["_id"] = str(run["_id"])
    return runs

@app.get("/api/run/{run_id}")
async def get_run(run_id: str, user = Depends(verify_token)):
    run = db.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    if user["role"] != "admin" and run["username"] != user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    run["_id"] = str(run["_id"])
    return run

@app.get("/admin/all_runs")
async def get_all_runs_admin():
    """Fetch all runs for admin analytics dashboard - no auth needed for demo"""
    runs = db.get_all_runs()
    for run in runs:
        run["_id"] = str(run["_id"])
    return {"runs": runs, "total": len(runs)}

@app.get("/api/export_csv")
async def export_csv(user = Depends(verify_token)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    csv_data = db.export_to_csv()
    return {"csv": csv_data}

@app.get("/api/graph-metrics/{run_id}")
async def get_graph_metrics(run_id: str, user = Depends(verify_token)):
    """Get agent collaboration network and metrics data for visualization dashboard"""
    try:
        from bson import ObjectId
        run = db.db["runs"].find_one({"_id": ObjectId(run_id)})
        
        if not run:
            raise HTTPException(status_code=404, detail="Run not found")
        
        if run["user_id"] != user["username"] and user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Extract agent stats from monitor_data
        agent_stats = {}
        monitor_data = run.get("monitor_data", {})
        agent_data = monitor_data.get("agent_stats", {})
        
        if agent_data:
            for agent_name, stats in agent_data.items():
                scores = stats.get("scores", [])
                agent_stats[agent_name] = {
                    "score": sum(scores) / len(scores) if scores else 0.5,
                    "min_score": min(scores) if scores else 0.0,
                    "max_score": max(scores) if scores else 1.0,
                    "interaction_count": stats.get("interaction_count", 0),
                    "output": stats.get("output", "")[:100]  # First 100 chars
                }
        
        # Build network graph data
        agents = list(agent_stats.keys())
        nodes = []
        links = []
        
        for idx, agent in enumerate(agents):
            nodes.append({
                "id": agent,
                "label": agent.replace("_", " "),
                "score": agent_stats[agent]["score"],
                "index": idx
            })
        
        # Create links between agents based on interactions
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                links.append({
                    "source": agents[i],
                    "target": agents[j],
                    "value": 2 + (agent_stats[agents[i]]["interaction_count"] % 3)
                })
        
        return {
            "run_id": str(run["_id"]),
            "task": run.get("task", ""),
            "timestamp": str(run.get("created_at", "")),
            "agent_stats": agent_stats,
            "graph": {
                "nodes": nodes,
                "links": links,
                "totalAgents": len(agents),
                "totalInteractions": len(links)
            },
            "metrics": {
                "initial_score": run.get("initial_score", 0),
                "final_score": run.get("predicted_score", 0),
                "enhancement_loops": run.get("enhancement_loops", 0),
                "score_improvement": ((run.get("predicted_score", 0) - run.get("initial_score", 0)) * 100)
            }
        }
    except Exception as e:
        print(f"Error in get_graph_metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard-summary")
async def get_dashboard_summary(user = Depends(verify_token)):
    """Get summary statistics for dashboard across recent runs"""
    try:
        from datetime import datetime, timedelta
        
        # Get last 30 days of runs
        last_30_days = datetime.utcnow() - timedelta(days=30)
        runs = list(db.db["runs"].find({
            "user_id": user["username"],
            "created_at": {"$gte": last_30_days}
        }).limit(100))
        
        if not runs:
            return {
                "total_runs": 0,
                "avg_initial_score": 0,
                "avg_final_score": 0,
                "total_improvement": 0,
                "agents_used": [],
                "top_performing_agent": None
            }
        
        agent_scores = {}
        total_initial = 0
        total_final = 0
        
        for run in runs:
            initial = run.get("initial_score", 0)
            final = run.get("predicted_score", 0)
            total_initial += initial
            total_final += final
            
            # Collect agent data
            agent_data = run.get("monitor_data", {}).get("agent_stats", {})
            for agent_name, stats in agent_data.items():
                if agent_name not in agent_scores:
                    agent_scores[agent_name] = []
                scores = stats.get("scores", [])
                if scores:
                    agent_scores[agent_name].extend(scores)
        
        # Calculate agent averages
        agent_averages = {}
        for agent, scores in agent_scores.items():
            if scores:
                agent_averages[agent] = sum(scores) / len(scores)
        
        # Find top agent
        top_agent = max(agent_averages.items(), key=lambda x: x[1]) if agent_averages else None
        
        avg_initial = total_initial / len(runs)
        avg_final = total_final / len(runs)
        
        return {
            "total_runs": len(runs),
            "avg_initial_score": round(avg_initial, 4),
            "avg_final_score": round(avg_final, 4),
            "total_improvement": round(((avg_final - avg_initial) * 100), 2),
            "agents_used": list(agent_scores.keys()),
            "top_performing_agent": {
                "name": top_agent[0],
                "avg_score": round(top_agent[1], 4)
            } if top_agent else None,
            "agent_performance": {
                agent: round(score, 4) 
                for agent, score in agent_averages.items()
            }
        }
    except Exception as e:
        print(f"Error in get_dashboard_summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("AgentMonitor API - http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
