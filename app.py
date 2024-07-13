from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('room_joined', {'room': room}, room=request.sid)
    print(f"User {request.sid} joined room {room}.")

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    emit('message', {'msg': msg}, room=room, include_self=False)

@socketio.on('disconnect')
def on_disconnect():
    print(f"User {request.sid} disconnected.")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
