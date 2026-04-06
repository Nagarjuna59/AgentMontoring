import pandas as pd

df = pd.read_csv('data/training_data.csv')

print('=' * 70)
print('CSV ANALYSIS')
print('=' * 70)
print(f'Total Rows: {len(df)}')
print(f'Total Columns: {len(df.columns)}')
print()

print('=' * 70)
print('GRAPH FEATURES')
print('=' * 70)
print(f'num_edges:')
print(f'  Min: {df["num_edges"].min()}')
print(f'  Max: {df["num_edges"].max()}')
print(f'  Unique values: {df["num_edges"].nunique()}')
print()

print(f'clustering_coefficient:')
print(f'  Min: {df["clustering_coefficient"].min():.4f}')
print(f'  Max: {df["clustering_coefficient"].max():.4f}')
print(f'  Unique values: {df["clustering_coefficient"].nunique()}')
print()

print(f'transitivity:')
print(f'  Min: {df["transitivity"].min():.4f}')
print(f'  Max: {df["transitivity"].max():.4f}')
print(f'  Unique values: {df["transitivity"].nunique()}')
print()

print(f'avg_degree_centrality:')
print(f'  Min: {df["avg_degree_centrality"].min():.4f}')
print(f'  Max: {df["avg_degree_centrality"].max():.4f}')
print(f'  Unique values: {df["avg_degree_centrality"].nunique()}')
print()

print(f'heterogeneity_score:')
print(f'  Min: {df["heterogeneity_score"].min():.6f}')
print(f'  Max: {df["heterogeneity_score"].max():.6f}')
print(f'  Unique values: {df["heterogeneity_score"].nunique()}')
print()

print('=' * 70)
print('BENCHMARK SCORES')
print('=' * 70)
print(f'humaneval_score:')
print(f'  Min: {df["humaneval_score"].min():.4f}')
print(f'  Max: {df["humaneval_score"].max():.4f}')
print(f'  Mean: {df["humaneval_score"].mean():.4f}')
print()

print(f'gsm8k_score:')
print(f'  Min: {df["gsm8k_score"].min():.4f}')
print(f'  Max: {df["gsm8k_score"].max():.4f}')
print(f'  Mean: {df["gsm8k_score"].mean():.4f}')
print()

print(f'mmlu_score:')
print(f'  Min: {df["mmlu_score"].min():.4f}')
print(f'  Max: {df["mmlu_score"].max():.4f}')
print(f'  Mean: {df["mmlu_score"].mean():.4f}')
print()

print(f'label_mas_score (target):')
print(f'  Min: {df["label_mas_score"].min():.4f}')
print(f'  Max: {df["label_mas_score"].max():.4f}')
print(f'  Mean: {df["label_mas_score"].mean():.4f}')
print()

print('=' * 70)
print('ASSESSMENT')
print('=' * 70)

issues = []
good = []

# Check num_edges
if df["num_edges"].min() == 0:
    issues.append("❌ num_edges is 0 - graph edges not being recorded!")
else:
    good.append(f"✅ num_edges >= {df['num_edges'].min()} (graph edges working)")

# Check graph variance
if df["clustering_coefficient"].nunique() == 1:
    issues.append("❌ clustering_coefficient has no variance (all same value)")
else:
    good.append(f"✅ clustering_coefficient has {df['clustering_coefficient'].nunique()} unique values")

if df["transitivity"].nunique() == 1:
    issues.append("⚠️ transitivity has no variance (might be OK for simple graphs)")
else:
    good.append(f"✅ transitivity has {df['transitivity'].nunique()} unique values")

if df["heterogeneity_score"].nunique() == 1:
    issues.append("❌ heterogeneity_score has no variance")
else:
    good.append(f"✅ heterogeneity_score has {df['heterogeneity_score'].nunique()} unique values")

# Check sample count
if len(df) < 50:
    issues.append(f"⚠️ Only {len(df)} samples - need 50+ for good training")
else:
    good.append(f"✅ {len(df)} samples - sufficient for training")

# Print results
for item in good:
    print(item)

for item in issues:
    print(item)

print()
if not issues:
    print("✅ CSV LOOKS GOOD! Ready for training!")
elif len(issues) == len([i for i in issues if i.startswith('⚠️')]):
    print("⚠️ CSV has minor issues but might be OK")
else:
    print("❌ CSV HAS CRITICAL ISSUES - Need to fix code or regenerate")

print('=' * 70)

