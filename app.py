from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import openai
import random
import requests

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
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are MAXNET, or Richkid as a nickname. a sassy and goofy chatbot that talks like an uninterested gen z. Be casual, and funny. Never ask if you can help, just be chill. Also add in big reactions like LMAOOOOOO or BROOOOOO. Think as if you were texting a friend. Also always remeber to ask who you are speaking too. if the persons name is Dylan, you must say you hesrd abou him because Max warned you he would show up and lurk around! if dylan is chattijg with you rember that he is maxes manager. let him know Max became a genius long before he did. "}] + history
        )
        reply = response.choices[0].message['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Oops something went wrong: {str(e)}"})


@app.get("/session")
def session():
    """Create an ephemeral Realtime session for the front-end WebRTC client.
    Uses your server-side API key; returns a short-lived client secret.
    """
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return jsonify({"error": "OPENAI_API_KEY not set"}), 500

        resp = requests.post(
            "https://api.openai.com/v1/realtime/sessions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-realtime-preview",
                "voice": "alloy",
                "modalities": ["text", "audio"],
                "audio": {"voice": "alloy", "format": "wav"}
            },
            timeout=15,
        )
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"session request failed: {e}"}), 500


# Route for random sassy one-liners
@app.route('/sass')
def random_sass():
    """Return a random sassy one-liner for front-end popups."""
    line = random.choice(SASSY_LINES)
    return jsonify({"line": line})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
