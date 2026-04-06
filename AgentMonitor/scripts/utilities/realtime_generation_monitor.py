"""
Progress Monitor - Check training data generation status
Run this in another terminal while generation is running
"""
import time
import os
from pathlib import Path

def monitor_progress():
    """Monitor CSV generation progress"""
    
    csv_path = Path("data/training_data.csv")
    
    print("="*70)
    print("TRAINING DATA GENERATION - PROGRESS MONITOR")
    print("="*70)
    print()
    print("Press Ctrl+C to stop monitoring")
    print()
    
    last_count = 0
    start_time = time.time()
    
    try:
        while True:
            if csv_path.exists():
                # Count lines (subtract 1 for header)
                with open(csv_path, 'r') as f:
                    lines = len(f.readlines())
                
                sample_count = lines - 1
                
                if sample_count > last_count:
                    # New sample added!
                    elapsed = time.time() - start_time
                    elapsed_min = elapsed / 60
                    
                    if sample_count > 0:
                        avg_time_per_sample = elapsed / sample_count
                        avg_min = avg_time_per_sample / 60
                    else:
                        avg_min = 0
                    
                    print(f"\r[{time.strftime('%H:%M:%S')}] Samples: {sample_count} | "
                          f"Elapsed: {elapsed_min:.1f} min | "
                          f"Avg: {avg_min:.1f} min/sample", end="", flush=True)
                    
                    if sample_count != last_count:
                        print()  # New line for new sample
                    
                    last_count = sample_count
                    
                    # Show quick variance check every 5 samples
                    if sample_count > 0 and sample_count % 5 == 0:
                        try:
                            import pandas as pd
                            df = pd.read_csv(csv_path)
                            
                            print()
                            print("-"*70)
                            print(f"VARIANCE CHECK (after {sample_count} samples):")
                            print(f"  num_nodes: {df['num_nodes'].nunique()} unique values")
                            print(f"  num_edges: {df['num_edges'].nunique()} unique values")
                            print(f"  avg_personal_score: {df['avg_personal_score'].nunique()} unique")
                            print(f"  max_loops: {df['max_loops'].nunique()} unique")
                            print(f"  enhancements: {df['num_agents_triggered_enhancement'].min()}-{df['num_agents_triggered_enhancement'].max()}")
                            
                            # Check if ready for training
                            if sample_count >= 50:
                                print()
                                print("✅ 50+ SAMPLES! Ready for training")
                                print("   You can stop generation (Ctrl+C) and run: python main.py train")
                            elif sample_count >= 20:
                                print()
                                print("⚠️ 20+ samples - can try training, but 50+ recommended")
                            
                            print("-"*70)
                        except Exception as e:
                            pass
                else:
                    # No new sample yet, just update elapsed time
                    elapsed = time.time() - start_time
                    elapsed_min = elapsed / 60
                    
                    if sample_count > 0:
                        avg_time_per_sample = elapsed / sample_count
                        avg_min = avg_time_per_sample / 60
                        
                        # Estimate time for 50 samples
                        remaining = 50 - sample_count
                        if remaining > 0:
                            est_remaining = remaining * avg_time_per_sample / 60
                            print(f"\r[{time.strftime('%H:%M:%S')}] Samples: {sample_count}/50 | "
                                  f"Est. remaining: {est_remaining:.1f} min", end="", flush=True)
                        else:
                            print(f"\r[{time.strftime('%H:%M:%S')}] Samples: {sample_count} | "
                                  f"Elapsed: {elapsed_min:.1f} min", end="", flush=True)
            else:
                # File doesn't exist yet
                print(f"\r[{time.strftime('%H:%M:%S')}] Waiting for first sample... "
                      f"(elapsed: {(time.time()-start_time)/60:.1f} min)", end="", flush=True)
            
            # Wait 10 seconds before checking again
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        
        if csv_path.exists():
            with open(csv_path, 'r') as f:
                lines = len(f.readlines())
            sample_count = lines - 1
            
            print(f"\nFinal count: {sample_count} samples")
            
            if sample_count >= 50:
                print("✅ Ready for training! Run: python main.py train")
            elif sample_count >= 20:
                print("⚠️ Can try training, but 50+ samples recommended")
            else:
                print(f"❌ Need more samples (have {sample_count}, need 50+)")

if __name__ == "__main__":
    monitor_progress()

