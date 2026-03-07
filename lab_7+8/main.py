"""
Lab 7 - Random Joke Flask App
Programming for Artificial Intelligence
Superior University Lahore

API Used: JokeAPI (https://v2.jokeapi.dev) - completely FREE, no API key needed!
"""

from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# JokeAPI base URL — free, no API key required
JOKE_API_BASE = "https://v2.jokeapi.dev/joke"

CATEGORIES = ["Any", "Programming", "Misc", "Dark", "Pun", "Spooky", "Christmas"]


def fetch_joke(category="Any", joke_type="any"):
    """Fetch a joke from JokeAPI"""
    try:
        url = f"{JOKE_API_BASE}/{category}"
        params = {
            "lang": "en",
            "blacklistFlags": "nsfw,explicit,racist,sexist",
        }
        if joke_type != "any":
            params["type"] = joke_type

        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get("error"):
            return None, data.get("message", "Unknown error")

        # Format joke based on type
        if data["type"] == "single":
            return {
                "type": "single",
                "joke": data["joke"],
                "category": data["category"],
                "id": data["id"],
                "flags": [k for k, v in data.get("flags", {}).items() if v]
            }, None
        else:
            return {
                "type": "twopart",
                "setup": data["setup"],
                "delivery": data["delivery"],
                "category": data["category"],
                "id": data["id"],
                "flags": [k for k, v in data.get("flags", {}).items() if v]
            }, None

    except requests.exceptions.ConnectionError:
        return None, "No internet connection. Check your network."
    except requests.exceptions.Timeout:
        return None, "Request timed out. Try again."
    except Exception as e:
        return None, str(e)


def fetch_ten_jokes(category="Any"):
    """Fetch up to 10 jokes at once"""
    try:
        url = f"{JOKE_API_BASE}/{category}"
        params = {
            "lang": "en",
            "blacklistFlags": "nsfw,explicit,racist,sexist",
            "amount": 10
        }
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        jokes = []
        raw_jokes = data.get("jokes", [data]) if "jokes" in data else [data]

        for d in raw_jokes:
            if d.get("error"):
                continue
            if d["type"] == "single":
                jokes.append({
                    "type": "single",
                    "joke": d["joke"],
                    "category": d["category"],
                    "id": d["id"]
                })
            else:
                jokes.append({
                    "type": "twopart",
                    "setup": d["setup"],
                    "delivery": d["delivery"],
                    "category": d["category"],
                    "id": d["id"]
                })
        return jokes, None

    except requests.exceptions.ConnectionError:
        return None, "No internet connection."
    except Exception as e:
        return None, str(e)


# ── ROUTES ──

@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES)


@app.route("/api/joke")
def get_joke():
    category  = request.args.get("category", "Any")
    joke_type = request.args.get("type", "any")

    if category not in CATEGORIES:
        category = "Any"

    joke, error = fetch_joke(category, joke_type)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"success": True, "joke": joke})


@app.route("/api/jokes/batch")
def get_batch_jokes():
    category = request.args.get("category", "Any")
    if category not in CATEGORIES:
        category = "Any"

    jokes, error = fetch_ten_jokes(category)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"success": True, "jokes": jokes, "count": len(jokes)})


@app.route("/api/categories")
def get_categories():
    return jsonify({"categories": CATEGORIES})


if __name__ == "__main__":
    print("😂 Random Joke App Starting...")
    print("   API: JokeAPI (https://v2.jokeapi.dev) - No key needed!")
    print("   Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
