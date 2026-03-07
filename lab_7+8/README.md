# GitHub Repository
> 🔗 **GitHub:** [Add your GitHub link here]

# Lab 7 — Random Joke Flask App
**Programming for Artificial Intelligence**
**Superior University Lahore**

## What This Project Does
A Flask web app that fetches random jokes from a free API (JokeAPI).
Filter by category and type, reveal punchlines, and load 10 jokes at once.

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
2. Select a **Category** (Any, Programming, Pun, Spooky, etc.)
3. Select a **Type** (Single line or Setup + Punchline)
4. Click **😂 Get a Joke!** or press `Enter`
5. For two-part jokes, click **🥁 Reveal Punchline**
6. Click **📦 Load 10 Jokes** to get a batch grid

---

## API Used
**JokeAPI** — https://v2.jokeapi.dev
- ✅ Completely free
- ✅ No API key required
- ✅ Returns JSON data

---

## Flask API Endpoints
| Route | Method | Description |
|---|---|---|
| `/` | GET | Main webpage |
| `/api/joke?category=Any&type=any` | GET | Get 1 joke |
| `/api/jokes/batch?category=Any` | GET | Get 10 jokes |
| `/api/categories` | GET | List all categories |

---

## Project Structure
```
lab7_joke_app/
├── main.py             ← Flask backend (calls JokeAPI)
├── pyproject.toml      ← uv dependencies
└── templates/
    └── index.html      ← Frontend UI
```

---

## How API Integration Works
```
Browser → Flask (/api/joke) → JokeAPI (https://v2.jokeapi.dev) → JSON → Browser
```
