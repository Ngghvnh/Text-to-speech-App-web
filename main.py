from flask import Flask, request, render_template, send_file
import requests
import io
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text")

    if not text:
        return "يرجى إدخال نص", 1500

    response = requests.post(
        "https://api.groq.com/openai/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "canopylabs/orpheus-arabic-saudi",
            "input": text,
            "voice": "amjad"
        }
    )

    if response.status_code != 200:
        return f"خطأ من API: {response.text}", 500

    return send_file(
        io.BytesIO(response.content),
        mimetype="audio/mpeg",
        as_attachment=True,
        download_name="speech.mp3"
    )

if __name__ == "__main__":
    app.run()