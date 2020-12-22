import socketio

sio = socketio.AsyncServer(cors_allowed_origins='*')


@sio.event
async def connect(sid, environ):
    sio.emit('connected', room=sid)


@sio.event
async def disconnect(sid):
    print('disconnect:', sid)
