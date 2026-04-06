from pymongo import MongoClient
from datetime import datetime
import hashlib
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self, connection_string=None):
        if connection_string is None:
            connection_string = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        
        self.client = MongoClient(connection_string)
        db_name = os.getenv("DATABASE_NAME", "agentmonitor")
        self.db = self.client[db_name]
        self.users = self.db["users"]
        self.runs = self.db["runs"]
        self.create_default_users()
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_users(self):
        if self.users.count_documents({}) == 0:
            self.users.insert_many([
                {"username": "admin", "password": self.hash_password("admin123"), "role": "admin", "created_at": datetime.now()},
                {"username": "user", "password": self.hash_password("user123"), "role": "user", "created_at": datetime.now()}
            ])
    
    def verify_user(self, username, password):
        user = self.users.find_one({"username": username, "password": self.hash_password(password)})
        return user
    
    def save_run(self, user_id, username, task, code, predicted_score, features, monitor_data, initial_code=None, initial_score=None):
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
