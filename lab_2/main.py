"""
Spaceship Titanic - Full ML Pipeline
Lab 2: Programming for Artificial Intelligence
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# STEP 1: LOAD DATA
# ─────────────────────────────────────────────
print("=" * 55)
print("  SPACESHIP TITANIC - ML PIPELINE")
print("=" * 55)

train = pd.read_csv("train.csv")
test  = pd.read_csv("test.csv")

print(f"\n✅ Train shape : {train.shape}")
print(f"✅ Test shape  : {test.shape}")

# ─────────────────────────────────────────────
# STEP 2: EXPLORATORY DATA ANALYSIS (EDA)
# ─────────────────────────────────────────────
print("\n--- STEP 2: EDA ---")
print("\nFirst 5 rows of training data:")
print(train.head())

print("\nMissing Values (Train):")
print(train.isnull().sum())

print("\nTarget Distribution:")
print(train['Transported'].value_counts())

# EDA PLOTS
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Exploratory Data Analysis - Spaceship Titanic", fontsize=16, fontweight='bold')

# 1. Target distribution
train['Transported'].value_counts().plot(kind='bar', ax=axes[0,0], color=['#E74C3C','#2ECC71'], edgecolor='black')
axes[0,0].set_title("Transported (Target) Distribution")
axes[0,0].set_xlabel("Transported")
axes[0,0].set_ylabel("Count")
axes[0,0].tick_params(axis='x', rotation=0)

# 2. Home Planet vs Transported
pd.crosstab(train['HomePlanet'], train['Transported']).plot(kind='bar', ax=axes[0,1], color=['#E74C3C','#2ECC71'], edgecolor='black')
axes[0,1].set_title("HomePlanet vs Transported")
axes[0,1].set_xlabel("Home Planet")
axes[0,1].tick_params(axis='x', rotation=0)

# 3. CryoSleep vs Transported
pd.crosstab(train['CryoSleep'], train['Transported']).plot(kind='bar', ax=axes[0,2], color=['#E74C3C','#2ECC71'], edgecolor='black')
axes[0,2].set_title("CryoSleep vs Transported")
axes[0,2].set_xlabel("CryoSleep")
axes[0,2].tick_params(axis='x', rotation=0)

# 4. Age distribution
train.groupby('Transported')['Age'].plot(kind='hist', ax=axes[1,0], alpha=0.6, bins=30, legend=True)
axes[1,0].set_title("Age Distribution by Transported")
axes[1,0].set_xlabel("Age")

# 5. Spending (RoomService) vs Transported
train.groupby('Transported')['RoomService'].plot(kind='hist', ax=axes[1,1], alpha=0.6, bins=30, legend=True)
axes[1,1].set_title("RoomService Spending by Transported")
axes[1,1].set_xlabel("Amount Spent")

# 6. Destination vs Transported
pd.crosstab(train['Destination'], train['Transported']).plot(kind='bar', ax=axes[1,2], color=['#E74C3C','#2ECC71'], edgecolor='black')
axes[1,2].set_title("Destination vs Transported")
axes[1,2].set_xlabel("Destination")
axes[1,2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("eda_plots.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ EDA plots saved!")

# ─────────────────────────────────────────────
# STEP 3: PREPROCESSING
# ─────────────────────────────────────────────
print("\n--- STEP 3: PREPROCESSING ---")

def preprocess(df):
    df = df.copy()

    # Split Cabin into Deck, Number, Side
    df[['Cabin_Deck', 'Cabin_Num', 'Cabin_Side']] = df['Cabin'].str.split('/', expand=True)

    # Drop columns not useful for model
    df.drop(columns=['PassengerId', 'Name', 'Cabin'], inplace=True)

    # Fill missing values
    # Numeric columns → fill with median
    num_cols = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 'Cabin_Num']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col].fillna(df[col].median(), inplace=True)

    # Categorical columns → fill with mode
    cat_cols = ['HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'Cabin_Deck', 'Cabin_Side']
    for col in cat_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # Encode boolean columns
    bool_cols = ['CryoSleep', 'VIP']
    for col in bool_cols:
        df[col] = df[col].map({'True': 1, 'False': 0, True: 1, False: 0}).fillna(0).astype(int)

    # Label encode remaining categoricals
    le = LabelEncoder()
    for col in ['HomePlanet', 'Destination', 'Cabin_Deck', 'Cabin_Side']:
        df[col] = le.fit_transform(df[col].astype(str))

    # Feature engineering: Total spending
    spend_cols = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
    df['TotalSpending'] = df[spend_cols].sum(axis=1)

    # Final catch-all fillna
    df.fillna(0, inplace=True)

    return df

train_processed = preprocess(train.drop(columns=['Transported']))
test_processed  = preprocess(test)

# Target variable
y = train['Transported'].astype(int)
X = train_processed

print(f"✅ Features shape: {X.shape}")
print(f"✅ Features used : {list(X.columns)}")

# ─────────────────────────────────────────────
# STEP 4: TRAIN / VALIDATION SPLIT
# ─────────────────────────────────────────────
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTrain size: {X_train.shape[0]}, Validation size: {X_val.shape[0]}")

# ─────────────────────────────────────────────
# STEP 5: TRAIN MODELS
# ─────────────────────────────────────────────
print("\n--- STEP 5: MODEL TRAINING & EVALUATION ---")

models = {
    "Naïve Bayes"     : GaussianNB(),
    "Decision Tree"   : DecisionTreeClassifier(random_state=42),
    "Random Forest"   : RandomForestClassifier(n_estimators=100, random_state=42)
}

results = {}
best_model = None
best_acc = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    acc = accuracy_score(y_val, preds)
    results[name] = acc
    print(f"\n{name}:")
    print(f"  Accuracy : {acc:.4f} ({acc*100:.2f}%)")
    print(f"  Report:\n{classification_report(y_val, preds, target_names=['Not Transported','Transported'])}")
    if acc > best_acc:
        best_acc = acc
        best_model = model
        best_name = name

print(f"\n🏆 Best Model: {best_name} with Accuracy = {best_acc*100:.2f}%")

# ─────────────────────────────────────────────
# STEP 6: CONFUSION MATRIX PLOT
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Confusion Matrices - All Models", fontsize=14, fontweight='bold')

for ax, (name, model) in zip(axes, models.items()):
    preds = model.predict(X_val)
    cm = confusion_matrix(y_val, preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['Not Transported','Transported'],
                yticklabels=['Not Transported','Transported'])
    acc = results[name]
    ax.set_title(f"{name}\nAccuracy: {acc*100:.1f}%")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

plt.tight_layout()
plt.savefig("confusion_matrices.png", dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Confusion matrix plot saved!")

# Model comparison bar chart
plt.figure(figsize=(8, 5))
colors = ['#3498DB', '#E67E22', '#2ECC71']
bars = plt.bar(results.keys(), [v*100 for v in results.values()], color=colors, edgecolor='black', width=0.5)
for bar, acc in zip(bars, results.values()):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f"{acc*100:.1f}%", ha='center', va='bottom', fontweight='bold')
plt.title("Model Accuracy Comparison", fontsize=14, fontweight='bold')
plt.ylabel("Accuracy (%)")
plt.ylim(0, 105)
plt.tight_layout()
plt.savefig("model_comparison.png", dpi=150, bbox_inches='tight')
plt.close()
print("✅ Model comparison chart saved!")

# ─────────────────────────────────────────────
# STEP 7: GENERATE SUBMISSION FILE
# ─────────────────────────────────────────────
print("\n--- STEP 7: GENERATING SUBMISSION FILE ---")

test_preds = best_model.predict(test_processed)
submission = pd.read_csv("sample_submission.csv")
submission['Transported'] = test_preds.astype(bool)
submission.to_csv("submission.csv", index=False)

print(f"✅ Submission file saved!")
print(f"   Predicted Transported=True  : {sum(test_preds)}")
print(f"   Predicted Transported=False : {len(test_preds) - sum(test_preds)}")

print("\n" + "="*55)
print("  PIPELINE COMPLETE!")
print("="*55)
