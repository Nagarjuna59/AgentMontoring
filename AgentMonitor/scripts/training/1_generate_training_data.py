"""
Dataset Generation Script
=========================
Purpose: Generate training data for XGBoost model using MAS variants

This script:
1. Creates diverse MAS variants (different thresholds, retries, architectures)
2. Runs each variant on random programming tasks
3. Monitors execution and extracts 16 behavioral features
4. Estimates quality using weak supervision (no benchmark execution)
5. Saves data incrementally to CSV for training

Usage:
    python generate_dataset.py
    
Output:
    ../data/training_data.csv - Training dataset with features and labels
"""

import sys
import os
import asyncio
import random
import pandas as pd
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from AgentMonitor import EnhancedAgentMonitor, CodeGenerationMAS, BenchmarkEvaluator


# Sample programming tasks for diverse dataset
SAMPLE_TASKS = [
    "Write a function to find the factorial of a number",
    "Implement a function to check if a string is a palindrome",
    "Create a function to find the nth Fibonacci number",
    "Write a function to reverse a linked list",
    "Implement binary search on a sorted array",
    "Create a function to merge two sorted arrays",
    "Write a function to find duplicates in an array",
    "Implement a stack using a list",
    "Create a function to validate parentheses in an expression",
    "Write a function to find the longest common substring",
    "Implement quicksort algorithm",
    "Create a function to detect cycle in a linked list",
    "Write a function to calculate power(x, n)",
    "Implement BFS traversal for a graph",
    "Create a function to find missing number in array",
    "Write a function to rotate an array by k positions",
    "Implement a queue using two stacks",
    "Create a function to find intersection of two arrays",
    "Write a function to check if binary tree is balanced",
    "Implement merge sort algorithm"
]


def get_random_mas_config():
    """Generate random MAS variant configuration"""
    return {
        'threshold': random.choice([0.5, 0.6, 0.7, 0.8]),
        'max_retries': random.choice([1, 2, 3]),
        'architecture': random.choice(['3-agent', '4-agent']),
        'monitor_threshold': random.choice([0.5, 0.6, 0.7]),
        'monitor_retries': random.choice([1, 2])
    }


async def generate_single_sample(task: str, mas_config: dict, sample_num: int):
    """Generate one training sample"""
    from gemini_api import gemini_call
    
    print(f"\n{'='*70}")
    print(f"SAMPLE {sample_num}: {task[:50]}...")
    print(f"{'='*70}")
    
    # Create monitor
    monitor = EnhancedAgentMonitor(
        threshold=mas_config['monitor_threshold'],
        max_enhancement_retries=mas_config['monitor_retries']
    )
    
    # Create MAS
    mas = CodeGenerationMAS(gemini_call, monitor)
    
    # Run MAS with monitoring
    print(f"🤖 Running {mas_config['architecture']} MAS...")
    result = await mas.run(task)
    monitor_data = monitor.get_summary()
    
    # Extract features
    print(f"📊 Extracting features...")
    evaluator = BenchmarkEvaluator()
    features = evaluator.extract_features(monitor_data)
    
    # Estimate quality (weak supervision)
    print(f"🎯 Estimating quality...")
    label = evaluator.estimate_benchmark_score(result, task)
    
    features['label_mas_score'] = label
    
    print(f"✅ Sample complete! Label: {label:.4f}")
    
    return features


async def generate_training_data(num_samples: int):
    """Generate multiple training samples"""
    csv_path = Path(__file__).parent.parent.parent / "data" / "training_data.csv"
    csv_path.parent.mkdir(exist_ok=True)
    
    print(f"\n{'='*70}")
    print(f"TRAINING DATA GENERATION")
    print(f"{'='*70}")
    print(f"Target samples: {num_samples}")
    print(f"Output: {csv_path}")
    print(f"{'='*70}\n")
    
    write_header = not csv_path.exists()
    
    for i in range(1, num_samples + 1):
        try:
            # Random task and config
            task = random.choice(SAMPLE_TASKS)
            mas_config = get_random_mas_config()
            
            # Generate sample
            features = await generate_single_sample(task, mas_config, i)
            
            # Save immediately (incremental append)
            df_row = pd.DataFrame([features])
            df_row.to_csv(csv_path, mode='a', header=write_header, index=False)
            write_header = False
            
            print(f"💾 Saved to CSV ({i}/{num_samples})")
            
        except Exception as e:
            print(f"❌ Error in sample {i}: {e}")
            continue
    
    # Final summary
    print(f"\n{'='*70}")
    print(f"GENERATION COMPLETE!")
    print(f"{'='*70}")
    
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"✅ Total samples: {len(df)}")
        print(f"✅ Features: {len(df.columns)}")
        print(f"✅ Location: {csv_path}")
    
    print(f"{'='*70}\n")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("MAS TRAINING DATA GENERATOR")
    print("="*70)
    
    num_samples = int(input("\nHow many samples to generate? "))
    
    asyncio.run(generate_training_data(num_samples))

