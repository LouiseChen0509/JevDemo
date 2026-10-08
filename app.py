import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

ENDPOINT = "https://ai-gateway.vercel.sh/typesafe/v1/systemone"


@app.get("/")
def health():
    return jsonify({
        "ok": True,
        "service": "JEV thesis gateway demo"
    })


@app.get("/api")
def test_jev():
    api_key = os.environ.get("AI_GATEWAY_API_KEY")

    if not api_key:
        return jsonify({
            "ok": False,
            "error": "AI_GATEWAY_API_KEY is not configured"
        }), 500

    payload = {
        "model": "typesafe-ai/jev",
        "state": "We are shown two items. Item 1 is 'apple'. Item 2 is 'truck'.",
        "questions": {
            "fruit": {
                "type": "choice",
                "instructions": "Which item is a fruit?",
                "criteria": {
                    "apple": "the item labelled 'apple'",
                    "truck": "the item labelled 'truck'"
                }
            }
        }
    }

    try:
        response = requests.post(
            ENDPOINT,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        return jsonify({
            "ok": True,
            "model": "typesafe-ai/jev",
            "answer": data.get("answers", {}).get("fruit", {}),
            "usage": data.get("usage", {})
        })

    except requests.RequestException as exc:
        return jsonify({
            "ok": False,
            "error": str(exc)
        }), 502
