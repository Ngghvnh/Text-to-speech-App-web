from flask import Flask, request, send_file, render_template_string
import requests
import io
import os

app = Flask(__name__)

# مفتاح Groq من Environment Variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# HTML مدمج داخل الكود (لا يحتاج templates folder)
html_code = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>تحويل النص إلى صوت</title>
<style>
body {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    font-family: Arial;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    color: white;
}
.container {
    background: rgba(0,0,0,0.6);
    padding: 40px;
    border-radius: 15px;
    width: 400px;
    text-align: center;
}
textarea {
    width: 100%;
    height: 120px;
    border-radius: 10px;
    padding: 10px;
    border: none;
    resize: none;
}
button {
    margin-top: 15px;
    padding: 12px;
    width: 100%;
    border: none;
    border-radius: 10px;
    background: #00c6ff;
    color: white;
    font-size: 16px;
    cursor: pointer;
}
button:hover {
    background: #0072ff;
}
</style>
</head>
<body>

<div class="container">
    <h2>🎤 تحويل النص إلى صوت</h2>
    <form action="/tts" method="POST">
        <textarea name="text" placeholder="اكتب النص هنا..." required></textarea>
        <button type="submit">تحويل إلى صوت</button>
    </form>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_code)

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text")

    if not text:
        return "يرجى إدخال نص", 400

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
    app.run(host="0.0.0.0", port=8080)
