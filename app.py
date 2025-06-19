from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# List of scripts
scripts = [
    {
        "filename": "WhyDidMyPuterCrashScript.sh",
        "title": "Crash Recovery Script",
        "description": "Diagnose why your puter had a mental breakdown 💀",
    },
    {
        "filename": "SlayStartupScript.sh",
        "title": "Slay Startup Script",
        "description": "Makes your Mac start up with ✨vibes✨. Also does cleanup.",
    },
    # Add more here!
]

@app.route('/')
def home():
    return render_template('index.html', scripts=scripts)

@app.route('/grab/<filename>')
def grab_script(filename):
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)