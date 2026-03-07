"""
House Price Prediction - Full ML Pipeline
Lab 1: Programming for Artificial Intelligence
Kaggle: https://www.kaggle.com/competitions/home-data-for-ml-course
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# STEP 1: LOAD DATA
# ─────────────────────────────────────────────
print("=" * 60)
print("   HOUSE PRICE PREDICTION - ML PIPELINE")
print("=" * 60)

train = pd.read_csv("train.csv")
test  = pd.read_csv("test.csv")

print(f"\n✅ Train shape : {train.shape}")
print(f"✅ Test shape  : {test.shape}")
print(f"\nTarget (SalePrice) Stats:")
print(train['SalePrice'].describe())

# ─────────────────────────────────────────────
# STEP 2: EDA
# ─────────────────────────────────────────────
print("\n--- STEP 2: EDA ---")

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle("Exploratory Data Analysis - House Price Prediction", fontsize=16, fontweight='bold')

# 1. Sale Price Distribution
axes[0,0].hist(train['SalePrice'], bins=50, color='#3498DB', edgecolor='black')
axes[0,0].set_title("Sale Price Distribution")
axes[0,0].set_xlabel("Sale Price ($)")
axes[0,0].set_ylabel("Count")

# 2. Sale Price (log) Distribution
axes[0,1].hist(np.log1p(train['SalePrice']), bins=50, color='#2ECC71', edgecolor='black')
axes[0,1].set_title("Sale Price Distribution (Log Scale)")
axes[0,1].set_xlabel("Log(Sale Price)")
axes[0,1].set_ylabel("Count")

# 3. Overall Quality vs Sale Price
train.groupby('OverallQual')['SalePrice'].median().plot(kind='bar', ax=axes[0,2], color='#E67E22', edgecolor='black')
axes[0,2].set_title("Overall Quality vs Median Sale Price")
axes[0,2].set_xlabel("Overall Quality (1-10)")
axes[0,2].set_ylabel("Median Sale Price ($)")
axes[0,2].tick_params(axis='x', rotation=0)

# 4. GrLivArea vs SalePrice scatter
axes[1,0].scatter(train['GrLivArea'], train['SalePrice'], alpha=0.4, color='#9B59B6')
axes[1,0].set_title("Living Area vs Sale Price")
axes[1,0].set_xlabel("Above Ground Living Area (sqft)")
axes[1,0].set_ylabel("Sale Price ($)")

# 5. Year Built vs Sale Price
train.groupby('YearBuilt')['SalePrice'].mean().plot(ax=axes[1,1], color='#E74C3C')
axes[1,1].set_title("Year Built vs Average Sale Price")
axes[1,1].set_xlabel("Year Built")
axes[1,1].set_ylabel("Average Sale Price ($)")

# 6. Top 10 Neighborhoods by median price
top_neigh = train.groupby('Neighborhood')['SalePrice'].median().sort_values(ascending=False).head(10)
top_neigh.plot(kind='bar', ax=axes[1,2], color='#1ABC9C', edgecolor='black')
axes[1,2].set_title("Top 10 Neighborhoods by Median Price")
axes[1,2].set_xlabel("Neighborhood")
axes[1,2].set_ylabel("Median Sale Price ($)")
axes[1,2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("house_eda_plots.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ EDA plots saved!")

# Correlation heatmap of numeric features
plt.figure(figsize=(14, 10))
numeric_cols = train.select_dtypes(include=[np.number]).columns.tolist()
corr = train[numeric_cols].corr()
# Show top 15 features most correlated with SalePrice
top_corr_features = corr['SalePrice'].abs().sort_values(ascending=False).head(15).index
sns.heatmap(train[top_corr_features].corr(), annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5)
plt.title("Correlation Heatmap - Top 15 Features", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("house_correlation_heatmap.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Correlation heatmap saved!")

# ─────────────────────────────────────────────
# STEP 3: PREPROCESSING
# ─────────────────────────────────────────────
print("\n--- STEP 3: PREPROCESSING ---")

# Missing value summary
missing = train.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
print(f"\nColumns with missing values: {len(missing)}")

def preprocess(df):
    df = df.copy()

    # Drop Id column
    df.drop(columns=['Id'], inplace=True, errors='ignore')

    # Feature Engineering
    df['HouseAge']      = df['YrSold'] - df['YearBuilt']
    df['RemodAge']      = df['YrSold'] - df['YearRemodAdd']
    df['TotalSF']       = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']
    df['TotalBath']     = df['FullBath'] + 0.5 * df['HalfBath'] + df['BsmtFullBath'] + 0.5 * df['BsmtHalfBath']
    df['TotalPorch']    = df['OpenPorchSF'] + df['EnclosedPorch'] + df['3SsnPorch'] + df['ScreenPorch']
    df['HasPool']       = (df['PoolArea'] > 0).astype(int)
    df['HasGarage']     = (df['GarageArea'] > 0).astype(int)
    df['HasFireplace']  = (df['Fireplaces'] > 0).astype(int)
    df['HasBasement']   = (df['TotalBsmtSF'] > 0).astype(int)

    # Fill missing values
    # Numeric → median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col].fillna(df[col].median(), inplace=True)

    # Categorical → mode or 'None'
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        df[col].fillna('None', inplace=True)

    # Label encode all categorical columns
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    return df

# Separate target
y = np.log1p(train['SalePrice'])  # log transform for better model performance
train_processed = preprocess(train.drop(columns=['SalePrice']))
test_processed  = preprocess(test)

# Align columns
train_processed, test_processed = train_processed.align(test_processed, join='left', axis=1, fill_value=0)
train_processed.fillna(0, inplace=True)
test_processed.fillna(0, inplace=True)

print(f"✅ Features shape : {train_processed.shape}")
print(f"✅ New features added: HouseAge, RemodAge, TotalSF, TotalBath, TotalPorch, HasPool, HasGarage, HasFireplace, HasBasement")

# ─────────────────────────────────────────────
# STEP 4: TRAIN / VALIDATION SPLIT
# ─────────────────────────────────────────────
X_train, X_val, y_train, y_val = train_test_split(train_processed, y, test_size=0.2, random_state=42)
print(f"\nTrain size: {X_train.shape[0]}, Validation size: {X_val.shape[0]}")

# ─────────────────────────────────────────────
# STEP 5: TRAIN MODELS
# ─────────────────────────────────────────────
print("\n--- STEP 5: MODEL TRAINING & EVALUATION ---")

models = {
    "Linear Regression"       : LinearRegression(),
    "Ridge Regression"        : Ridge(alpha=10),
    "Decision Tree"           : DecisionTreeRegressor(random_state=42, max_depth=10),
    "Random Forest"           : RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting"       : GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, random_state=42)
}

results = {}
best_model = None
best_rmse = float('inf')
best_name = ""

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_val)

    # Convert back from log scale
    actual_prices  = np.expm1(y_val)
    predicted_prices = np.expm1(preds)

    mae  = mean_absolute_error(actual_prices, predicted_prices)
    rmse = np.sqrt(mean_squared_error(actual_prices, predicted_prices))
    r2   = r2_score(actual_prices, predicted_prices)

    results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}

    print(f"\n{name}:")
    print(f"  MAE  : ${mae:,.0f}")
    print(f"  RMSE : ${rmse:,.0f}")
    print(f"  R²   : {r2:.4f}")

    if rmse < best_rmse:
        best_rmse = rmse
        best_model = model
        best_name = name

print(f"\n🏆 Best Model: {best_name}")
print(f"   RMSE = ${best_rmse:,.0f} | R² = {results[best_name]['R2']:.4f}")

# ─────────────────────────────────────────────
# STEP 6: PLOTS - Model Comparison & Feature Importance
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Model Performance Comparison", fontsize=14, fontweight='bold')

model_names = list(results.keys())
rmse_vals = [results[m]['RMSE'] for m in model_names]
r2_vals   = [results[m]['R2']   for m in model_names]
colors = ['#3498DB','#2ECC71','#E67E22','#E74C3C','#9B59B6']

bars = axes[0].bar(model_names, rmse_vals, color=colors, edgecolor='black')
for bar, val in zip(bars, rmse_vals):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
                 f"${val:,.0f}", ha='center', va='bottom', fontsize=8, fontweight='bold')
axes[0].set_title("RMSE Comparison (lower is better)")
axes[0].set_ylabel("RMSE ($)")
axes[0].tick_params(axis='x', rotation=15)

bars2 = axes[1].bar(model_names, r2_vals, color=colors, edgecolor='black')
for bar, val in zip(bars2, r2_vals):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                 f"{val:.3f}", ha='center', va='bottom', fontsize=8, fontweight='bold')
axes[1].set_title("R² Score (higher is better)")
axes[1].set_ylabel("R² Score")
axes[1].set_ylim(0, 1.05)
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig("house_model_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Model comparison plot saved!")

# Feature Importance (from best tree model)
if hasattr(best_model, 'feature_importances_'):
    importance_df = pd.DataFrame({
        'Feature': train_processed.columns,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False).head(20)

    plt.figure(figsize=(10, 8))
    plt.barh(importance_df['Feature'][::-1], importance_df['Importance'][::-1], color='#3498DB', edgecolor='black')
    plt.title(f"Top 20 Feature Importances ({best_name})", fontsize=13, fontweight='bold')
    plt.xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig("house_feature_importance.png", dpi=150, bbox_inches='tight')
    plt.close()
    print("✅ Feature importance plot saved!")

# Actual vs Predicted plot
preds_val = np.expm1(best_model.predict(X_val))
actual_val = np.expm1(y_val)
plt.figure(figsize=(8, 6))
plt.scatter(actual_val, preds_val, alpha=0.4, color='#2ECC71')
plt.plot([actual_val.min(), actual_val.max()], [actual_val.min(), actual_val.max()], 'r--', lw=2, label='Perfect Prediction')
plt.xlabel("Actual Price ($)")
plt.ylabel("Predicted Price ($)")
plt.title(f"Actual vs Predicted Prices ({best_name})", fontsize=13, fontweight='bold')
plt.legend()
plt.tight_layout()
plt.savefig("house_actual_vs_predicted.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Actual vs Predicted plot saved!")

# ─────────────────────────────────────────────
# STEP 7: GENERATE SUBMISSION FILE
# ─────────────────────────────────────────────
print("\n--- STEP 7: GENERATING SUBMISSION FILE ---")

test_preds = np.expm1(best_model.predict(test_processed))
submission = pd.read_csv("sample_submission.csv")
submission['SalePrice'] = test_preds
submission.to_csv("house_submission.csv", index=False)

print(f"✅ Submission file saved!")
print(f"   Predicted Price Range: ${test_preds.min():,.0f} — ${test_preds.max():,.0f}")
print(f"   Average Predicted Price: ${test_preds.mean():,.0f}")

print("\n" + "="*60)
print("  PIPELINE COMPLETE!")
print("="*60)
