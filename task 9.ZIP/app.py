from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob

nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

app = Flask(__name__)

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()
    task = data.get("task", "tokenize")

    if not text:
        return jsonify({"error": "Please enter some text first."}), 400

    if task == "tokenize":
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        return jsonify({
            "words": words,
            "sentences": sentences,
            "word_count": len(words),
            "sentence_count": len(sentences)
        })

    elif task == "stopwords":
        words = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        filtered = [w for w in words if w.lower() not in stop_words]
        removed = [w for w in words if w.lower() in stop_words]
        return jsonify({
            "original": words,
            "filtered": filtered,
            "removed": removed
        })

    elif task == "stemming":
        words = word_tokenize(text)
        stemmed = [(w, stemmer.stem(w)) for w in words if w.isalpha()]
        return jsonify({"pairs": stemmed})

    elif task == "lemmatization":
        words = word_tokenize(text)
        lemmatized = [(w, lemmatizer.lemmatize(w)) for w in words if w.isalpha()]
        return jsonify({"pairs": lemmatized})

    elif task == "sentiment":
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"

        return jsonify({
            "label": label,
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3)
        })

    return jsonify({"error": "Unknown task."}), 400

if __name__ == "__main__":
    app.run(debug=True)
