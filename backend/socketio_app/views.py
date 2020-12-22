import socketio

sio = socketio.Server(cors_allowed_origins='*')


async def connect(sid, environ):
    sio.emit('connected', room=sid)


async def disconnect(sid):
    print('disconnect:', sid)
