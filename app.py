import os
import json
from flask import Flask, request, jsonify, render_template

from summarizer import generate_summary, load_dotenv

app = Flask(__name__)

# Load env variables on startup
load_dotenv()

# We can default to the provided deployment properties
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://dt-ai-foundry-demo-01-rg.cognitiveservices.azure.com/")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.4-pro")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "transcript" not in data:
        return jsonify({"error": "Missing 'transcript' in request body"}), 400
    
    transcript = data["transcript"]
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "Server is missing AZURE_OPENAI_API_KEY environment variable. Please set it in .env"}), 500

    try:
        summary_text = generate_summary(
            transcript=transcript,
            endpoint=AZURE_ENDPOINT,
            api_key=api_key,
            deployment=AZURE_DEPLOYMENT,
            api_version=AZURE_API_VERSION,
            max_output_tokens=2000
        )
        
        # Try to parse it as JSON so we can send a proper JSON response rather than a stringified JSON
        try:
            summary_json = json.loads(summary_text)
            return jsonify(summary_json)
        except json.JSONDecodeError:
            return jsonify({"raw_text": summary_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
