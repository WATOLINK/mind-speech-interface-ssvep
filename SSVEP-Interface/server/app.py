from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import requests

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
thread = None
thread_lock = Lock()

def background_thread():
    while True:
        data = requests.get('https://api.kanye.rest')
        socketio.emit('response', data.json())
        socketio.sleep(5)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('client_message')
def handle_client_message(data):
    socketio.emit('response', data)

@socketio.event
def connect():
    print('Connected...')
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)

if __name__ == '__main__':
    socketio.run(app)