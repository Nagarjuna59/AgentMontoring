"""
Interactive MAS Auto-Improvement (Production)
=============================================
Purpose: Automatically optimize MAS performance for user tasks

This is the main production file for interactive use with auto-improvement.
It tries different MAS variants and keeps the best result based on predicted scores.

Features:
- Takes user programming tasks
- Tries up to 3 different MAS variants
- Predicts quality after each attempt
- Automatically stops when score ≥ 0.75
- Returns best result

Usage:
    python interactive.py
    
Requirements:
    - Trained model at models/mas_predictor.pkl
    - Gemini API key in .env file
"""

import sys
import asyncio
import pickle
import random
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from AgentMonitor import EnhancedAgentMonitor, CodeGenerationMAS, FeatureExtractor
from gemini_api import gemini_call


# Configuration
SCORE_THRESHOLD = 0.75  # Stop if predicted score >= this
MAX_ATTEMPTS = 3        # Maximum optimization attempts


def get_random_mas_variant():
    """Generate random MAS configuration for diversity"""
    return {
        'monitor_threshold': random.choice([0.5, 0.6, 0.7]),
        'monitor_retries': random.choice([1, 2]),
        'mas_threshold': random.choice([0.5, 0.6, 0.7, 0.8]),
        'mas_retries': random.choice([1, 2, 3])
    }


async def run_mas_with_prediction(task: str, variant_config: dict):
    """
    Run MAS and predict quality
    
    Args:
        task: Programming task
        variant_config: MAS variant configuration
        
    Returns:
        tuple: (predicted_score, features, result)
    """
    # Create monitor with variant config
    monitor = EnhancedAgentMonitor(
        threshold=variant_config['monitor_threshold'],
        max_retries=variant_config['monitor_retries']
    )
    
    # Create and run MAS
    mas = CodeGenerationMAS(gemini_call, monitor)
    result = await mas.run(task)
    monitor_data = monitor.get_summary()
    
    # Extract features
    feature_extractor = FeatureExtractor()
    features = feature_extractor.extract_all_features(monitor_data)
    
    # Load model and predict
    model_path = Path(__file__).parent / "models" / "mas_predictor.pkl"
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    
    FEATURE_COLUMNS = [
        "avg_personal_score", "min_personal_score", "max_loops",
        "total_latency", "total_token_usage", "num_agents_triggered_enhancement",
        "num_nodes", "num_edges", "clustering_coefficient", "transitivity",
        "avg_degree_centrality", "avg_betweenness_centrality", "avg_closeness_centrality",
        "pagerank_entropy", "heterogeneity_score", "collective_score"
    ]
    
    import numpy as np
    X = np.array([[features[col] for col in FEATURE_COLUMNS]])
    predicted_score = model.predict(X)[0]
    
    return predicted_score, features, result


async def auto_improve_task(task: str):
    """
    Auto-improve: Try different MAS variants until quality threshold met
    
    Args:
        task: Programming task
        
    Returns:
        tuple: (best_score, best_features, best_result)
    """
    print(f"\n{'='*70}")
    print(f"AUTO-IMPROVEMENT MODE")
    print(f"{'='*70}")
    print(f"Task: {task[:60]}...")
    print(f"Threshold: {SCORE_THRESHOLD}")
    print(f"Max Attempts: {MAX_ATTEMPTS}")
    print(f"{'='*70}\n")
    
    best_score = 0
    best_features = None
    best_result = None
    
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n{'='*70}")
        print(f"🔄 ATTEMPT {attempt}/{MAX_ATTEMPTS}")
        print(f"{'='*70}\n")
        
        # Generate random variant
        variant = get_random_mas_variant()
        print(f"📊 MAS Variant:")
        print(f"   Monitor threshold: {variant['monitor_threshold']}")
        print(f"   Monitor retries: {variant['monitor_retries']}")
        print(f"   MAS threshold: {variant['mas_threshold']}")
        print(f"   MAS retries: {variant['mas_retries']}\n")
        
        try:
            # Run and predict
            predicted_score, features, result = await run_mas_with_prediction(task, variant)
            
            print(f"\n🎯 Predicted Score: {predicted_score:.4f}")
            print(f"📊 Agents: {features.get('num_nodes', 0)}, Edges: {features.get('num_edges', 0)}")
            print(f"⏱️  Latency: {features.get('total_latency', 0):.2f}s")
            
            # Update best if better
            if predicted_score > best_score:
                best_score = predicted_score
                best_features = features
                best_result = result
                print(f"✅ NEW BEST SCORE!")
            
            # Stop if threshold met
            if predicted_score >= SCORE_THRESHOLD:
                print(f"\n🎉 Score above threshold ({SCORE_THRESHOLD})! Stopping.")
                break
                
        except Exception as e:
            print(f"❌ Error in attempt {attempt}: {e}")
            continue
    
    # Display best result
    print(f"\n{'='*70}")
    print(f"🏆 BEST RESULT (after {min(attempt, MAX_ATTEMPTS)} attempt(s))")
    print(f"{'='*70}")
    print(f"🎯 FINAL PREDICTED SCORE: {best_score:.4f}")
    print(f"{'='*70}\n")
    
    print(f"📊 KEY FEATURES:")
    print(f"   Agents: {best_features.get('num_nodes', 0)}")
    print(f"   Edges: {best_features.get('num_edges', 0)}")
    print(f"   Avg Agent Score: {best_features.get('avg_personal_score', 0):.4f}")
    print(f"   Enhancement Loops: {best_features.get('max_loops', 0)}")
    print(f"   Total Latency: {best_features.get('total_latency', 0):.2f}s\n")
    
    print(f"📝 BEST MAS OUTPUT:")
    print(f"{'='*70}")
    print(best_result)
    print(f"{'='*70}\n")
    
    return best_score, best_features, best_result


async def main():
    """Main interactive loop"""
    print("\n" + "="*70)
    print("INTERACTIVE MAS AUTO-IMPROVEMENT")
    print("="*70)
    print("Enter tasks and get optimized code automatically!")
    print(f"System tries up to {MAX_ATTEMPTS} variants, keeps best result.")
    print("="*70 + "\n")
    
    # Check model exists
    model_path = Path(__file__).parent / "models" / "mas_predictor.pkl"
    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        print(f"   Run: python scripts/training/train_model.py")
        return
    
    print(f"[LOADED] Model loaded from {model_path}\n")
    
    while True:
        task = input("Enter programming task (or 'exit'): ").strip()
        
        if task.lower() in ['exit', 'quit']:
            print("\n👋 Goodbye!\n")
            break
        
        if not task:
            print("⚠️  Please enter a task.\n")
            continue
        
        try:
            await auto_improve_task(task)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())

