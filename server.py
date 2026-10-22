"""Flask web interface for the Emotion Detector."""

from flask import Flask, render_template, request
from emotion_detection import emotion_detector

app = Flask(__name__)

# Lightweight keyword-based fallback for demonstrations when the course API
# is unreachable. This is an estimate, not the Watson model.
KEYWORDS = {
    "anger": {"angry", "anger", "furious", "annoyed", "hate", "irritated", "mad"},
    "disgust": {"disgust", "gross", "awful", "nasty", "revolting"},
    "fear": {"afraid", "fear", "scared", "terrified", "worried", "anxious", "nervous"},
    "joy": {"happy", "joy", "excited", "love", "great", "wonderful", "delighted", "glad", "amazing"},
    "sadness": {"sad", "sadness", "unhappy", "depressed", "lonely", "heartbroken", "cry"},
}


def local_estimate(text):
    """Produce a clearly labeled, simple keyword-based demo estimate."""
    words = {word.strip(".,!?;:()[]{}\"'").lower() for word in text.split()}
    counts = {emotion: sum(word in keywords for word in words)
              for emotion, keywords in KEYWORDS.items()}
    total = sum(counts.values())
    if total == 0:
        scores = {emotion: 0.2 for emotion in KEYWORDS}
        dominant = "neutral"
    else:
        # Keep scores normalized for an easy-to-read demo.
        scores = {emotion: count / total for emotion, count in counts.items()}
        dominant = max(scores, key=scores.get)
    return {
        "anger": scores["anger"],
        "disgust": scores["disgust"],
        "fear": scores["fear"],
        "joy": scores["joy"],
        "sadness": scores["sadness"],
        "dominant_emotion": dominant,
        "source": "local",
    }


@app.route("/", methods=["GET", "POST"])
def index():
    """Display the input form and process submitted text."""
    result = None
    error = None
    submitted_text = ""

    if request.method == "POST":
        submitted_text = request.form.get("text", "").strip()
        if not submitted_text:
            error = "Please enter a sentence before analyzing."
        else:
            result = emotion_detector(submitted_text)
            if result.get("dominant_emotion") is None:
                result = local_estimate(submitted_text)
            else:
                result["source"] = "watson"

    return render_template(
        "index.html",
        result=result,
        error=error,
        submitted_text=submitted_text,
    )


if __name__ == "__main__":
    app.run(debug=False)
