"""
Dataset Quality Checker
========================
Analyzes training dataset quality and readiness for XGBoost training

Usage:
    python check_dataset.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def check_dataset():
    """Check dataset quality"""
    csv_path = Path(__file__).parent.parent.parent / "data" / "training_data.csv"
    
    print("\n" + "="*70)
    print("DATASET QUALITY CHECKER")
    print("="*70)
    
    if not csv_path.exists():
        print(f"❌ Dataset not found at {csv_path}")
        print(f"   Run: python scripts/training/generate_dataset.py")
        return
    
    df = pd.read_csv(csv_path)
    
    print(f"\n📊 Basic Statistics:")
    print(f"   Total samples: {len(df)}")
    print(f"   Total columns: {len(df.columns)}")
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"\n⚠️  Missing Values:")
        for col in missing[missing > 0].index:
            print(f"   {col}: {missing[col]}")
    else:
        print(f"\n✅ No missing values")
    
    # Check variance
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\n📈 Feature Variance:")
    
    low_variance = []
    for col in numeric_cols:
        if col not in ['label_mas_score', 'true_benchmark_score']:
            std = df[col].std()
            if std < 0.01:
                low_variance.append(col)
                print(f"   ⚠️  {col}: {std:.6f} (LOW VARIANCE)")
            else:
                print(f"   ✅ {col}: {std:.4f}")
    
    # Label distribution
    print(f"\n🎯 Label Distribution:")
    print(f"   Min: {df['label_mas_score'].min():.4f}")
    print(f"   Max: {df['label_mas_score'].max():.4f}")
    print(f"   Mean: {df['label_mas_score'].mean():.4f}")
    print(f"   Std: {df['label_mas_score'].std():.4f}")
    
    # Recommendations
    print(f"\n{'='*70}")
    print(f"RECOMMENDATIONS")
    print(f"{'='*70}")
    
    if len(df) < 50:
        print(f"⚠️  Only {len(df)} samples. Recommended: 100+ for good model")
    elif len(df) < 100:
        print(f"⚠️  {len(df)} samples. Recommended: 150+ for better model")
    else:
        print(f"✅ {len(df)} samples - Good for training!")
    
    if low_variance:
        print(f"⚠️  {len(low_variance)} features have low variance")
        print(f"   This may reduce model performance")
    else:
        print(f"✅ All features have sufficient variance")
    
    if df['label_mas_score'].std() < 0.05:
        print(f"⚠️  Labels have low variance - may need more diverse tasks")
    else:
        print(f"✅ Labels have good variance")
    
    print(f"\n{'='*70}")
    
    if len(df) >= 50 and len(low_variance) < 5:
        print(f"✅ DATASET READY FOR TRAINING!")
        print(f"   Run: python scripts/training/train_model.py")
    else:
        print(f"⚠️  Dataset needs improvement")
        print(f"   Run: python scripts/training/generate_dataset.py")
    
    print(f"{'='*70}\n")


if __name__ == "__main__":
    check_dataset()

