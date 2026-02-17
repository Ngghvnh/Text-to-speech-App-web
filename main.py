from flask import Flask, request, send_file, render_template_string
import requests
import io
import os

app = Flask(__name__)

# مفتاح Groq من Environment Variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# قائمة الأصوات المتاحة
voices = ["fahad", "sultan", "noura", "lulwa", "aisha"]

# عينات صوتية ثابتة لكل صوت (روابط WAV مثال)
voice_samples = {
    "fahad": "https://example.com/samples/fahad.wav",
    "sultan": "https://example.com/samples/sultan.wav",
    "noura": "https://example.com/samples/noura.wav",
    "lulwa": "https://example.com/samples/lulwa.wav",
    "aisha": "https://example.com/samples/aisha.wav"
}

# HTML مدمج داخل main.py
html_code = """
<!DOCTYPE html>
<html lang="ar">
<head>
<meta charset="UTF-8">
<title>تحويل النص إلى صوت</title>
<style>
body {background:linear-gradient(135deg,#1e3c72,#2a5298);font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;color:white;}
.container {background:rgba(0,0,0,0.6);padding:30px;border-radius:15px;width:400px;text-align:center;}
textarea {width:100%;height:100px;border-radius:10px;padding:10px;border:none;resize:none;}
select, button {margin-top:10px;padding:10px;width:100%;border:none;border-radius:10px;font-size:16px;cursor:pointer;}
button {background:#00c6ff;color:white;}
button:hover {background:#0072ff;}
.sample {margin-top:10px;text-align:left;}
.sample strong {display:inline-block;width:70px;}
audio {width:calc(100% - 80px);vertical-align:middle;}
</style>
</head>
<body>
<div class="container">
<h2>🎤 تحويل النص إلى صوت</h2>
<form action="/tts" method="POST">
<textarea name="text" placeholder="اكتب النص هنا..." required maxlength="1200"></textarea>
<select name="voice">
{% for v in voices %}
<option value="{{v}}">{{v.capitalize()}}</option>
{% endfor %}
</select>
<button type="submit">تحويل إلى صوت</button>
</form>

<h3>🎧 عينات الأصوات</h3>
{% for v,sample in voice_samples.items() %}
<div class="sample">
<strong>{{v.capitalize()}}</strong>
<audio controls>
<source src="{{sample}}" type="audio/wav">
المتصفح لا يدعم تشغيل الصوت
</audio>
</div>
{% endfor %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_code, voices=voices, voice_samples=voice_samples)

@app.route("/tts", methods=["POST"])
def tts():
    text = request.form.get("text")
    voice = request.form.get("voice")

    if not text or voice not in voices:
        return "يرجى إدخال نص واختيار صوت صحيح", 400

    # قص النص إذا تجاوز 1200 حرف لتجنب خطأ Groq المجانية
    text = text[:1200]

    response = requests.post(
        "https://api.groq.com/openai/v1/audio/speech",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "canopylabs/orpheus-arabic-saudi",
            "input": text,
            "voice": voice,
            "response_format": "wav"
        }
    )

    if response.status_code != 200:
        return f"خطأ من واجهة برمجة التطبيقات: {response.text}", 500

    return send_file(
        io.BytesIO(response.content),
        mimetype="audio/wav",
        as_attachment=True,
        download_name=f"{voice}_speech.wav"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
