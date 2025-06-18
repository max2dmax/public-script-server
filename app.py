from flask import Flask, send_from_directory
import os 

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome to Max’s Script Server 😎</h1><p><a href="/grab-script">Grab the script here</a></p>'

@app.route('/grab-script')
def grab_script():
    return send_from_directory('static', 'WhyDidMyPuterCrashScript.sh', as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)