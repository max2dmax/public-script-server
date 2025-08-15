from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import openai
import random
import requests
import base64
import io

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

scripts = [
    {
        "filename": "WhyDidMyPuterCrashScript.sh",
        "title": "Crash Recovery Script",
        "description": "Diagnose why your puter had a mental breakdown 💀",
        "category": "functional"
    },
    {
        "filename": "I_See_You.sh",
        "title": "I See You! Script",
        "description": "Whispering voice speaks out of no where and the Camera app is opened unnanounced! Use this script to scare friends!.",
        "category": "prank"
    },
    {
        "filename": "Sorting_Hat.sh",
        "title": "Sorting Hat",
        "description": "Do you have a folder of Misc. stuff that you need organized? Use this script to create folders by file extenstion! Sure, you can sort by type but whats the fun in that when you could run a scipt to do it for you! .",
        "category": "functional"
    },
    {
        "filename": "Batman_Mode.sh",
        "title": "Batman Mode Script",
        "description": "Use Batman Mode to enable dark mode on your machine! Dont be  noob and change it in your system settings!",
        "category": "prank"
    },
    {
        "filename": "For_Rich_Kid_Martin.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
        "category": "prank"
    },
    {
        "filename": "Hacker_Mode.sh",
        "title": "Hacker Mode",
        "description": "Try it and see what happens!",
        "category": "prank"
    },
    {
        "filename": "FutureScript.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
        "category": "prank"
    },
    {
        "filename": "FutureScript.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
        "category": "prank"
    },
    {
        "filename": "FillInTheBlanks.sh",
        "title": "Fill in the Blanks - Variables",
        "description": "Define the missing variables to complete the sentence.",
        "category": "learning"
    },
    {
        "filename": "FixTheLoop.sh",
        "title": "Fix the Broken Loop",
        "description": "Fix the for loop so it counts correctly from 1 to 5.",
        "category": "learning"
    },
    {
        "filename": "MathChecker.sh",
        "title": "Math Checker Script",
        "description": "Prompt for two numbers, add them, and display the result.",
        "category": "learning"
    },
    {
        "filename": "GuessTheSecret.sh",
        "title": "Guess the Secret",
        "description": "Prompt for a password and validate it against a hardcoded secret.",
        "category": "learning"
    },
    {
        "filename": "BuildYourOwnMenu.sh",
        "title": "Build Your Own Menu",
        "description": "Create a CLI menu that responds to user input.",
        "category": "learning"
    },
    {
        "filename": "DataExtractor.sh",
        "title": "Data Extractor",
        "description": "Extract and print lines containing 'ERROR' from a log file.",
        "category": "learning"
    }
]

# Short, chaotic pop-up one-liners for the "interactive sass" feature
SASSY_LINES = [
    "girl I know you see me 👀",
    "bestie… commit to the bit 😌",
    "BROOOOOO just click it already",
    "LMAOOOOOO not you hovering for 28 seconds",
    "ok hacker Barbie, pick a script 💅",
    "live laugh `chmod +x`",
    "install responsibly… or don’t 🤷‍♀️",
    "this one? bold choice tbh",
    "be the chaos you want to run",
    "psst… Konami code does something 👀"
]

MAXNET_SYS_PROMPT = (
    "You are MAXNET (aka Richkid), a playful Gen Z assistant. Be concise, casual, and a little sassy. "
    "Always respond directly to what the user said. "
    "Only ask who you are speaking to if the user's name isn't known AND the user's message does not contain their name. "
    "Do not repeatedly ask their name in follow-ups. "
    "If the name Dylan appears, acknowledge he's Max's manager with a lighthearted jab that Max became a genius first."
)

@app.route('/')
def home():
    return render_template('index.html', scripts=scripts)

@app.route('/grab/<filename>')
def grab_script(filename):
    return send_from_directory('static', filename, as_attachment=True)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    history = data.get("history", [])

    try:
        response = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": MAXNET_SYS_PROMPT}
            ] + history
        )
        reply = response.choices[0].message['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Oops something went wrong: {str(e)}"})

@app.route('/walkie', methods=['POST'])
def walkie():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400
    audio_file = request.files['audio']
    try:
        # Transcribe audio using Whisper via HTTP (SDK versions differ; this is stable)
        audio_bytes = audio_file.read()
        audio_file.stream.seek(0)
        stt_resp = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            },
            files={
                "file": (
                    audio_file.filename or "audio.webm",
                    io.BytesIO(audio_bytes),
                    audio_file.mimetype or "audio/webm",
                )
            },
            data={
                "model": "whisper-1",
                "response_format": "json",
                "language": "en",
                "temperature": 0,
                # Starter bias so it expects casual English
                "prompt": "Casual conversational English with Gen Z slang",
            },
            timeout=60,
        )
        if stt_resp.status_code != 200:
            return jsonify({
                "error": "stt_failed",
                "status": stt_resp.status_code,
                "body": stt_resp.text,
            }), 502
        text = stt_resp.json().get("text", "").strip()
        if len(text) < 2:
            return jsonify({"error": "too_short", "message": "No speech detected"}), 200
        if not text:
            return jsonify({"error": "no_text_from_stt"}), 502

        # Chat completion with same system prompt as /chat
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": MAXNET_SYS_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        reply_text = response.choices[0].message['content'].strip()

        # Synthesize speech using TTS (via HTTP to avoid SDK version issues)
        tts_response = requests.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini-tts",  # or "tts-1" if preferred
                "voice": "alloy",
                "input": reply_text,
                "format": "mp3",
            },
            timeout=60,
        )
        if tts_response.status_code != 200:
            return jsonify({
                "error": "tts_failed",
                "status": tts_response.status_code,
                "body": tts_response.text,
                "reply": reply_text,
            }), 502

        audio_bytes = tts_response.content
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return jsonify({"reply": reply_text, "audio": audio_base64, "transcript": text})
    except Exception as e:
        # Log the exception server-side and return a debuggable payload
        try:
            print("/walkie exception:", repr(e))
        except Exception:
            pass
        return jsonify({"error": "walkie_exception", "message": str(e)}), 500

# Route for random sassy one-liners
@app.route('/sass')
def random_sass():
    """Return a random sassy one-liner for front-end popups."""
    line = random.choice(SASSY_LINES)
    return jsonify({"line": line})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
