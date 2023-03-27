from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from game.core import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command')
def handle_command(command):
    response = game.process_command(command)
    emit('response', response)

def run_server():
    socketio.run(app, debug=True)

if __name__ == '__main__':
    run_server()
