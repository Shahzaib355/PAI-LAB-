# GitHub Repository
> 🔗 **GitHub:** [Add your GitHub link here]

# Lab 2 — Spaceship Titanic (Classification)
**Programming for Artificial Intelligence**
**Superior University Lahore**

## What This Project Does
Predicts which passengers were "transported" to another dimension.
Trains 3 classification models and generates a Kaggle submission file.

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
| `eda_plots.png` | 6 EDA charts |
| `confusion_matrices.png` | Confusion matrix for each model |
| `model_comparison.png` | Accuracy bar chart |
| `submission.csv` | Upload this to Kaggle |

---

## Models Trained
| Model | Accuracy |
|---|---|
| Naïve Bayes | 70.04% |
| Decision Tree | 75.68% |
| Random Forest | 79.30% ✅ Best |

---

## Dataset
Download from: https://www.kaggle.com/competitions/spaceship-titanic
