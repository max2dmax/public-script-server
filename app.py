from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

scripts = [
    {
        "filename": "WhyDidMyPuterCrashScript.sh",
        "title": "Crash Recovery Script",
        "description": "Diagnose why your puter had a mental breakdown 💀",
    },
    {
        "filename": "I_See_You.sh",
        "title": "I See You! Script",
        "description": "Whispering voice speaks out of no where and the Camera app is opened unnanounced! Use this script to scare friends!.",
    },
    {
        "filename": "Sorting_Hat.sh",
        "title": "Sorting Hat",
        "description": "Do you have a folder of Misc. stuff that you need organized? Use this script to create folders by file extenstion! Sure, you can sort by type but whats the fun in that when you could run a scipt to do it for you! .",
    },
    {
        "filename": "Batman_Mode.sh",
        "title": "Batman Mode Script",
        "description": "Use Batman Mode to enable dark mode on your machine! Dont be  noob and change it in your system settings!",
    },
    {
        "filename": "For_Rich_Kid_Martin.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
    },
    {
        "filename": "FutureScrip.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
    },
    {
        "filename": "FutureScript.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
    },
    {
        "filename": "FutureScript.sh",
        "title": "Rich Kid Martin's Script",
        "description": "Hey Rich kid! Use this script as a template to create whatever script you want! Just remember.. I NEVER helped you!",
    }
##  TEsting


@app.route('/')
def home():
    return render_template('index.html', scripts=scripts)

@app.route('/grab/<filename>')
def grab_script(filename):
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)