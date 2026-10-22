"""Emotion detection using the Watson NLP Emotion Prediction API."""

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
API_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Return a consistent empty result when analysis cannot be completed."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the supplied text."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            API_URL,
            headers=API_HEADERS,
            json=payload,
            timeout=30,
        )
        if response.status_code == 400:
            return _empty_result()

        response.raise_for_status()
        data = response.json()
        emotions = data["emotionPredictions"][0]["emotion"]

        scores = {key: float(emotions[key]) for key in EMOTION_KEYS}
        scores["dominant_emotion"] = max(
            EMOTION_KEYS, key=scores.get
        )
        return scores
    except (
        requests.RequestException,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
    ):
        return _empty_result()
