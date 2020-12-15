from aiohttp import web
from aiohttp_middlewares import cors_middleware
from socketio import AsyncServer
import json
import re
import ssl
from config import *

app = web.Application(middlewares=[
    cors_middleware(
        allow_all=True,
        urls=[re.compile(r'(?!\/socket.io\/)')]
    )
])
sio = AsyncServer(cors_allowed_origins='*')
sio.attach(app)

# api
def get_params(request):
    try:
        if not (content := request.content):
            raise Exception
        return json.loads(vars(content).get('_buffer', ['{}']).pop())
    except AttributeError:
        return {}

async def send_packet(request):
    params = get_params(request)
    await sio.emit('send_packet', params)
    return web.Response(text=json.dumps({ 'status': 'success' }), content_type='application/json')

# service api
app.router.add_post('/packet', send_packet)

if __name__ == '__main__':
    web.run_app(app, port=SERVER_PORT)
