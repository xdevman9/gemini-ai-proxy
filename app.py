import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativeai.googleapis.com/v1beta3/models/gemini-1.5-pro:generateText"


if not GEMINI_API_KEY:
    raise ValueError("Gemini API key is missing from environment variables.")

@app.route('/proxy', methods=['POST'])
def proxy():
    user_input = request.json.get("input", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

  
    payload = {
        "input": user_input,
        "temperature": 1.0,
        "maxOutputTokens": 1024,
        "topP": 0.95,
        "topK": 40
    }


    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

  
    try:
        response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
        response.raise_for_status()  
        data = response.json()

        return jsonify({
            "response": data.get("text", "No text returned from Gemini API.")
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request to Gemini API failed: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
