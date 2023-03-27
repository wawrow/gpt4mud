from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from game.core import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    join_room('game')
    emit('response', game.add_player(request.sid))

@socketio.on('disconnect')
def handle_disconnect():
    game.remove_player(request.sid)
    leave_room('game')

@socketio.on('command')
def handle_command(command):
    response = game.process_command(request.sid, command)
    emit('response', response)

def run_server():
    socketio.run(app, debug=True)

if __name__ == '__main__':
    run_server()
