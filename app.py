from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome to Max’s Script Server 😎</h1><p><a href="/grab-script">Grab the script here</a></p>'

@app.route('/grab-script')
def grab_script():
    return send_from_directory('static', 'your_script.py', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)