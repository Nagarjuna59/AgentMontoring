"""
Model Training Script
====================
Purpose: Train XGBoost model on collected MAS behavioral data

This script:
1. Loads training data from CSV
2. Splits into train/test sets (80/20)
3. Trains XGBoost regressor on 16 behavioral features
4. Evaluates using Spearman correlation
5. Saves trained model to file

Usage:
    python train_model.py
    
Input:
    ../data/training_data.csv - Dataset with features and labels
    
Output:
    ../models/mas_predictor.pkl - Trained XGBoost model
"""

import sys
import pickle
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from AgentMonitor import MASPredictor


def train_model():
    """Train XGBoost model on MAS data"""
    
    # Paths
    data_path = Path(__file__).parent.parent.parent / "data" / "training_data.csv"
    model_path = Path(__file__).parent.parent.parent / "models" / "mas_predictor.pkl"
    model_path.parent.mkdir(exist_ok=True)
    
    print("\n" + "="*70)
    print("XGBOOST MODEL TRAINING")
    print("="*70)
    print(f"Data: {data_path}")
    print(f"Model output: {model_path}")
    print("="*70 + "\n")
    
    # Check data exists
    if not data_path.exists():
        print(f"❌ Error: Training data not found at {data_path}")
        print(f"   Run generate_dataset.py first to create training data.")
        return
    
    # Train model
    print("🤖 Training XGBoost model...\n")
    
    predictor = MASPredictor(model_path=model_path)
    metrics = predictor.train(
        data_path=data_path,
        test_size=0.2,
        cv_folds=5,
        tune_hyperparams=False,  # Set to True for hyperparameter tuning
        save_model=True
    )
    
    # Display results
    print("\n" + "="*70)
    print("TRAINING COMPLETE!")
    print("="*70)
    print(f"✅ Model saved to: {model_path}")
    print(f"\n📊 Performance Metrics:")
    print(f"   Training Spearman: {metrics.get('train_spearman', 0):.4f}")
    print(f"   Test Spearman: {metrics.get('test_spearman', 0):.4f}")
    print(f"   Training R²: {metrics.get('train_r2', 0):.4f}")
    print(f"   Test R²: {metrics.get('test_r2', 0):.4f}")
    print(f"   Test MAE: {metrics.get('test_mae', 0):.4f}")
    print("="*70 + "\n")
    
    # Feature importance
    if 'feature_importance' in metrics:
        print("📈 Top 10 Important Features:")
        importance = metrics['feature_importance'].head(10)
        for idx, row in importance.iterrows():
            print(f"   {row['feature']:30s} {row['importance']:.4f}")
        print()


if __name__ == "__main__":
    train_model()

