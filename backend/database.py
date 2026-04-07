from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        
        self.client = MongoClient(connection_string)
        db_name = os.getenv("DB_NAME", "agentmonitor")
        self.db = self.client[db_name]
        self.users = self.db["users"]
        self.runs = self.db["runs"]
        self.cache = self.db["llm_cache"]  # NEW: Cache collection
        self.create_default_users()
        self._ensure_cache_index()
    
    def _ensure_cache_index(self):
        """Create indexes for cache collection."""
        try:
            self.cache.create_index("prompt_hash", unique=True)
            self.cache.create_index("created_at", expireAfterSeconds=86400)  # 24hr TTL
        except:
            pass
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _hash_prompt(self, prompt: str) -> str:
        """Generate hash for prompt to use as cache key."""
        # Normalize prompt to improve cache hits
        normalized = prompt.strip().lower()
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def get_cached_response(self, prompt: str) -> str | None:
        """Get cached LLM response for a prompt."""
        prompt_hash = self._hash_prompt(prompt)
        cached = self.cache.find_one({"prompt_hash": prompt_hash})
        if cached:
            # Update access time
            self.cache.update_one(
                {"_id": cached["_id"]},
                {"$set": {"last_accessed": datetime.now()}, "$inc": {"hit_count": 1}}
            )
            return cached.get("response")
        return None
    
    def cache_response(self, prompt: str, response: str):
        """Cache an LLM response."""
        prompt_hash = self._hash_prompt(prompt)
        try:
            self.cache.update_one(
                {"prompt_hash": prompt_hash},
                {
                    "$set": {
                        "prompt_hash": prompt_hash,
                        "prompt_preview": prompt[:200],  # Store preview for debugging
                        "response": response,
                        "created_at": datetime.now(),
                        "last_accessed": datetime.now()
                    },
                    "$setOnInsert": {"hit_count": 0}
                },
                upsert=True
            )
        except:
            pass
    
    def get_similar_task_code(self, task: str) -> dict | None:
        """Find similar completed task from history to reuse code."""
        # Simple keyword matching - find runs with similar task
        keywords = task.lower().split()[:5]  # First 5 words
        if not keywords:
            return None
        
        # Search for completed runs with similar tasks
        query = {
            "status": "done",
            "code": {"$exists": True, "$ne": ""},
            "$or": [{"task": {"$regex": kw, "$options": "i"}} for kw in keywords if len(kw) > 3]
        }
        
        similar = self.runs.find_one(query, sort=[("predicted_score", -1)])
        if similar and similar.get("code"):
            return {
                "brute_code": similar.get("brute_code", similar.get("code")),
                "semi_code": similar.get("semi_code", similar.get("code")),
                "optimal_code": similar.get("optimal_code", similar.get("code")),
                "code": similar.get("code"),
                "predicted_score": similar.get("predicted_score", 0.85)
            }
        return None
    
    def create_default_users(self):
        if self.users.count_documents({}) == 0:
            self.users.insert_many([
                {"username": "admin", "password": self.hash_password("admin123"), "role": "admin", "created_at": datetime.now()},
                {"username": "user", "password": self.hash_password("user123"), "role": "user", "created_at": datetime.now()}
            ])
    
    def verify_user(self, username, password):
        user = self.users.find_one({"username": username, "password": self.hash_password(password)})
        return user
    
    def save_run(self, user_id, username, task, code, predicted_score, features, monitor_data, initial_code=None, initial_score=None, **extra_fields):
        run = {
            "user_id": str(user_id),
            "username": username,
            "task": task,
            "code": code,  # Final/enhanced code
            "initial_code": initial_code,  # Store initial code separately
            "predicted_score": predicted_score,
            "initial_score": initial_score,  # Store initial score
            "features": features,
            "monitor_data": monitor_data,
            "created_at": datetime.now()
        }
        if extra_fields:
            run.update(extra_fields)
        return self.runs.insert_one(run).inserted_id

    def update_run(self, run_id, updates: dict):
        """Update a run document by its ObjectId (run_id can be string or ObjectId)."""
        from bson import ObjectId
        oid = ObjectId(run_id) if not isinstance(run_id, ObjectId) else run_id
        updates['updated_at'] = datetime.now()
        self.runs.update_one({"_id": oid}, {"$set": updates})
        return self.get_run(run_id)
    
    def get_run(self, run_id):
        from bson import ObjectId
        return self.runs.find_one({"_id": ObjectId(run_id)})
    
    def get_user_runs(self, username):
        return list(self.runs.find({"username": username}).sort("created_at", -1))
    
    def get_all_runs(self):
        return list(self.runs.find().sort("created_at", -1))
    
    def export_to_csv(self):
        runs = list(self.runs.find())
        df = pd.DataFrame(runs)
        return df.to_csv(index=False)
