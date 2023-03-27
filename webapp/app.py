from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def run_server():
    socketio.run(app, debug=True)

if __name__ == '__main__':
    run_server()
