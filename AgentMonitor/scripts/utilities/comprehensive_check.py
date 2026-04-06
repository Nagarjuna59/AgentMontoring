import pandas as pd
import numpy as np

df = pd.read_csv('data/training_data.csv')

print('=' * 70)
print('COMPREHENSIVE CSV ASSESSMENT FOR XGBOOST TRAINING')
print('=' * 70)
print()

# 1. Sample Size
print('1. SAMPLE SIZE')
print(f'   Rows: {len(df)}')
if len(df) < 20:
    print('   ❌ CRITICAL: Need at least 20-50 samples for XGBoost')
elif len(df) < 50:
    print('   ⚠️ WARNING: Need 50+ samples for reliable training')
else:
    print('   ✅ Sufficient samples')
print()

# 2. Feature Variance
print('2. FEATURE VARIANCE (Can XGBoost learn from this?)')
print()
features = [col for col in df.columns if col not in ['humaneval_score', 'gsm8k_score', 'mmlu_score', 'label_mas_score']]

constant_features = []
low_variance_features = []
good_features = []

for feat in features:
    unique_vals = df[feat].nunique()
    variance = df[feat].var()
    
    if unique_vals == 1:
        constant_features.append(feat)
        print(f'   ❌ {feat}: CONSTANT (all same value)')
    elif variance < 0.01:
        low_variance_features.append(feat)
        print(f'   ⚠️ {feat}: Low variance ({variance:.6f})')
    else:
        good_features.append(feat)
        print(f'   ✅ {feat}: Good variance ({variance:.2f})')

print()
print(f'   Summary:')
print(f'   - Constant features: {len(constant_features)} (XGBoost will ignore)')
print(f'   - Low variance: {len(low_variance_features)} (might be ignored)')
print(f'   - Usable features: {len(good_features)} (XGBoost can learn)')
print()

# 3. Target Variable
print('3. TARGET VARIABLE (label_mas_score)')
print(f'   Min: {df["label_mas_score"].min():.4f}')
print(f'   Max: {df["label_mas_score"].max():.4f}')
print(f'   Range: {df["label_mas_score"].max() - df["label_mas_score"].min():.4f}')
print(f'   Std Dev: {df["label_mas_score"].std():.4f}')
print(f'   Variance: {df["label_mas_score"].var():.6f}')

if df["label_mas_score"].var() < 0.001:
    print('   ❌ CRITICAL: Target has almost no variance!')
elif df["label_mas_score"].var() < 0.01:
    print('   ⚠️ WARNING: Target has low variance')
else:
    print('   ✅ Target has good variance')
print()

# 4. Feature-Target Correlation
print('4. FEATURE-TARGET CORRELATION')
print('   (Which features might predict the target?)')
print()

correlations = []
for feat in good_features:
    corr = df[feat].corr(df['label_mas_score'])
    correlations.append((feat, abs(corr)))
    if abs(corr) > 0.5:
        print(f'   ✅ {feat}: {corr:.3f} (strong)')
    elif abs(corr) > 0.3:
        print(f'   ⚠️ {feat}: {corr:.3f} (moderate)')
    else:
        print(f'   ❌ {feat}: {corr:.3f} (weak)')

print()
if correlations:
    best_feat, best_corr = max(correlations, key=lambda x: x[1])
    print(f'   Best predictor: {best_feat} (correlation: {best_corr:.3f})')
else:
    print('   ⚠️ No features with variance!')
print()

# 5. Missing Values
print('5. DATA QUALITY')
missing = df.isnull().sum().sum()
print(f'   Missing values: {missing}')
if missing > 0:
    print('   ❌ Has missing values - need to handle')
else:
    print('   ✅ No missing values')
print()

# 6. Overall Assessment
print('=' * 70)
print('FINAL ASSESSMENT')
print('=' * 70)
print()

issues = []
warnings = []
goods = []

# Check sample size
if len(df) < 20:
    issues.append('Sample size too small (need 20+ minimum)')
elif len(df) < 50:
    warnings.append(f'Only {len(df)} samples (50+ recommended)')
else:
    goods.append(f'{len(df)} samples available')

# Check usable features
if len(good_features) == 0:
    issues.append('No features with variance - XGBoost cannot learn!')
elif len(good_features) < 3:
    warnings.append(f'Only {len(good_features)} usable features (low predictive power)')
else:
    goods.append(f'{len(good_features)} features with variance')

# Check target variance
if df["label_mas_score"].var() < 0.001:
    issues.append('Target variable has no variance')
elif df["label_mas_score"].var() < 0.01:
    warnings.append('Target variable has low variance')
else:
    goods.append('Target has good variance')

# Check correlations
if correlations and max(correlations, key=lambda x: x[1])[1] < 0.3:
    warnings.append('Weak feature-target correlations')
elif correlations:
    goods.append('Some features correlate with target')

# Print results
if goods:
    print('✅ GOOD:')
    for g in goods:
        print(f'   • {g}')
    print()

if warnings:
    print('⚠️ WARNINGS:')
    for w in warnings:
        print(f'   • {w}')
    print()

if issues:
    print('❌ CRITICAL ISSUES:')
    for i in issues:
        print(f'   • {i}')
    print()

# Final verdict
print('=' * 70)
if issues:
    print('VERDICT: ❌ NOT READY FOR TRAINING')
    print('Action: Fix critical issues first')
elif warnings and len(warnings) > 2:
    print('VERDICT: ⚠️ CAN TRY TRAINING BUT EXPECT POOR RESULTS')
    print('Action: Generate more samples or add variance')
elif warnings:
    print('VERDICT: ⚠️ TRAINING POSSIBLE BUT SUBOPTIMAL')
    print('Action: Consider generating more samples')
else:
    print('VERDICT: ✅ READY FOR TRAINING')
    print('Action: Proceed with python main.py train')
print('=' * 70)

