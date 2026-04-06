"""
MAS Quality Prediction (Production)
===================================
Purpose: Predict MAS performance without running benchmarks

This is the main production file for fast MAS quality prediction.
It runs a MAS on a task, extracts behavioral features, and predicts
the quality score using the trained XGBoost model.

Usage:
    python predict.py
    
    Then enter any programming task when prompted.
    
Requirements:
    - Trained model at models/mas_predictor.pkl
    - Gemini API key in .env file
"""

import sys
import asyncio
import pickle
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from AgentMonitor import EnhancedAgentMonitor, CodeGenerationMAS, FeatureExtractor
from gemini_api import gemini_call


async def predict_mas_quality(task: str):
    """
    Predict MAS quality for a given task
    
    Args:
        task: Programming task description
        
    Returns:
        tuple: (predicted_score, features, mas_output)
    """
    print(f"\n{'='*70}")
    print(f"TASK: {task}")
    print(f"{'='*70}\n")
    
    # Step 1: Run MAS with monitoring
    print("🤖 Running MAS with monitoring...")
    monitor = EnhancedAgentMonitor(threshold=0.6, max_retries=1)
    mas = CodeGenerationMAS(gemini_call, monitor)
    
    result = await mas.run(task)
    monitor_data = monitor.get_summary()
    
    # Display monitor summary
    print("\n" + "="*70)
    print("MAS EXECUTION COMPLETE")
    print("="*70)
    print(f"Agents: {monitor_data.get('total_agents', 0)}")
    print(f"Enhancements: {monitor_data.get('total_enhancements', 0)}")
    print(f"Avg Score: {monitor_data.get('avg_agent_score', 0):.4f}")
    print("="*70 + "\n")
    
    # Step 2: Extract features
    print("📊 Extracting behavioral features...")
    feature_extractor = FeatureExtractor()
    features = feature_extractor.extract_all_features(monitor_data)
    
    # Step 3: Load model and predict
    print("🤖 Loading XGBoost model...")
    model_path = Path(__file__).parent / "models" / "mas_predictor.pkl"
    
    if not model_path.exists():
        print(f"❌ Model not found at {model_path}")
        print(f"   Run: python scripts/training/train_model.py")
        return None, None, None
    
    with open(model_path, 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    
    # Prepare features for prediction
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
    
    # Display results
    print(f"\n{'='*70}")
    print(f"🎯 PREDICTED MAS SCORE: {predicted_score:.4f}")
    print(f"{'='*70}\n")
    
    print(f"📊 Key Features:")
    print(f"   Agents: {features.get('num_nodes', 0)}")
    print(f"   Graph Edges: {features.get('num_edges', 0)}")
    print(f"   Avg Agent Score: {features.get('avg_personal_score', 0):.4f}")
    print(f"   Total Latency: {features.get('total_latency', 0):.2f}s")
    print(f"   Enhancements: {features.get('max_loops', 0)}")
    
    print(f"\n{'='*70}")
    print(f"MAS OUTPUT:")
    print(f"{'='*70}")
    print(result)
    print(f"{'='*70}\n")
    
    return predicted_score, features, result


async def main():
    """Main prediction loop"""
    print("\n" + "="*70)
    print("MAS QUALITY PREDICTOR")
    print("="*70)
    print("Predict MAS performance without running benchmarks!")
    print("="*70 + "\n")
    
    while True:
        task = input("Enter programming task (or 'exit'): ").strip()
        
        if task.lower() in ['exit', 'quit']:
            print("\n👋 Goodbye!\n")
            break
        
        if not task:
            print("⚠️  Please enter a task.\n")
            continue
        
        try:
            await predict_mas_quality(task)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())

