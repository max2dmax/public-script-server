from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import openai

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
            messages=history
        )
        reply = response.choices[0].message['content'].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Oops something went wrong: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)