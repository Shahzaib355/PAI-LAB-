# GitHub Repository
> 🔗 **GitHub:** [Add your GitHub link here]

# Lab 6 — Animal Herd Detection Flask App
**Programming for Artificial Intelligence**
**Superior University Lahore**

## What This Project Does
A Flask web app that detects animals in uploaded images using OpenCV.
Shows detection count, herd status, alert level, and marks location on a map.

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

Then open `http://localhost:5000` in your browser.

---

## How to Use
1. Open `http://localhost:5000`
2. Click the upload zone or drag & drop an animal image
3. Click **Run Herd Detection**
4. View results — bounding boxes, animal count, alert level
5. Scroll down to see the **Map Alert** (OpenStreetMap)

---

## Alert Levels
| Animals Detected | Status | Alert |
|---|---|---|
| 0 | No Animals | None |
| 1 – 2 | Small Group | 🟢 Low |
| 3 – 7 | Medium Herd | 🟡 Medium |
| 8+ | Large Herd | 🔴 High |

---

## Project Structure
```
lab6_herd_detection/
├── main.py             ← Flask backend
├── pyproject.toml      ← uv dependencies
├── templates/
│   └── index.html      ← Frontend UI
├── uploads/            ← Auto-created on first run
└── results/            ← Auto-created on first run
```

---

## Bonus Feature
Uses **OpenStreetMap (Leaflet.js)** — free, no API key needed —
to show a simulated GPS location of where the herd was detected.
