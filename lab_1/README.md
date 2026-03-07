# GitHub Repository
> 🔗 **GitHub:** [Add your GitHub link here]

# Lab 1 — House Price Prediction
**Programming for Artificial Intelligence**
**Superior University Lahore**

## What This Project Does
Predicts house sale prices using machine learning.
Trains 5 models and generates a Kaggle submission file.

---

## Setup & Run

### Step 1: Install uv
```bash
pip install uv
```

### Step 2: Install dependencies & Run
```bash
uv sync
uv run python3 main.py
```

---

## Output Files Generated
| File | Description |
|---|---|
| `house_eda_plots.png` | 6 EDA charts |
| `house_correlation_heatmap.png` | Feature correlation heatmap |
| `house_model_comparison.png` | Model accuracy comparison |
| `house_actual_vs_predicted.png` | Predicted vs actual prices |
| `house_submission.csv` | Upload this to Kaggle |

---

## Models Trained
| Model | Result |
|---|---|
| Linear Regression | Best — R² = 0.91 |
| Ridge Regression | R² = 0.90 |
| Random Forest | R² = 0.89 |
| Gradient Boosting | R² = 0.89 |
| Decision Tree | R² = 0.78 |

---

## Dataset
Download from: https://www.kaggle.com/competitions/home-data-for-ml-course
