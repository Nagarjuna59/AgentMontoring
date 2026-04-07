"""
Clear MongoDB cache of failed/error results
Run this to reset the cache when LLM configuration changes
"""
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()

def clear_cache():
    """Clear all cached responses from database"""
    db = Database()
    
    print("=" * 60)
    print("CACHE CLEARING UTILITY")
    print("=" * 60)
    
    # Count runs with errors
    try:
        collection = db.db["runs"]
        
        # Find runs with generation failures
        error_runs = list(collection.find({
            "$or": [
                {"code": {"$regex": "Generation failed"}},
                {"status": "failed"},
                {"brute_code": {"$regex": "Generation failed"}}
            ]
        }))
        
        print(f"\nFound {len(error_runs)} runs with errors")
        
        if len(error_runs) > 0:
            response = input("Delete these failed runs? (yes/no): ").strip().lower()
            
            if response == "yes":
                result = collection.delete_many({
                    "$or": [
                        {"code": {"$regex": "Generation failed"}},
                        {"status": "failed"},
                        {"brute_code": {"$regex": "Generation failed"}}
                    ]
                })
                print(f"✅ Deleted {result.deleted_count} failed runs")
            else:
                print("Skipped deletion")
        
        # Optional: clear ALL cache
        print("\n" + "-" * 60)
        total_runs = collection.count_documents({})
        print(f"Total runs in database: {total_runs}")
        
        if total_runs > 0:
            response = input("\nClear ALL runs (full cache reset)? (yes/no): ").strip().lower()
            
            if response == "yes":
                result = collection.delete_many({})
                print(f"✅ Deleted all {result.deleted_count} runs")
            else:
                print("Keeping other runs")
        
        print("\n" + "=" * 60)
        print("✅ Cache cleanup complete!")
        print("=" * 60)
        print("\nNow restart the backend:")
        print("   1. Stop backend (Ctrl+C)")
        print("   2. Run: python app.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure MongoDB is accessible")

if __name__ == "__main__":
    clear_cache()
