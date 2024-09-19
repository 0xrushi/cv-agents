import asyncio
import json
import base64
from aiohttp import web
from aiohttp import WSMsgType
import websockets
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume.generator import generate_from_data

connected_clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    print('Client connected')
    connected_clients.add(ws)

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                data = json.loads(msg.data)
                if data['type'] == 'json':
                    print('Received JSON update:', data['content'])
                    # Broadcast to all clients
                    for client in connected_clients:
                        await client.send_json({'type': 'json', 'content': data['content']})
                elif data['type'] == 'pdf':
                    print('Received PDF request')
                    pdf_path = data.get('path')
                    if pdf_path:
                        with open(path, 'rb') as file:
                            pdf_content = await file.read()
                        
                        await ws.send_bytes(pdf_content)
                        print(f'Sent PDF to client (size: {len(pdf_content)} bytes)')
                    else:
                        await ws.send_json({'type': 'error', 'message': 'PDF path not provided'})
            elif msg.type == WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {ws.exception()}')
    finally:
        connected_clients.remove(ws)
        print('Client disconnected')

    return ws

async def send_json(request):
    new_data = await request.json()
    
    for client in connected_clients:
        await client.send_json({'type': 'json', 'content': new_data})
    
    return web.Response(status=200)

async def send_pdf(request):
    try:
        data = await request.json()
        pdf_path = data['path']
        
        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()
        
        base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
        
        for client in connected_clients:
            await client.send_json({'type': 'pdf', 'content': base64_pdf})
        
        return web.Response(status=200)
    except Exception as e:
        print('Error reading PDF:', str(e))
        return web.Response(status=500, text='Error reading PDF')

async def init_app():
    app = web.Application()
    app.router.add_get('/ws', websocket_handler)
    app.router.add_post('/sendjson', send_json)
    app.router.add_post('/sendpdf', send_pdf)
    return app

if __name__ == '__main__':
    app = asyncio.get_event_loop().run_until_complete(init_app())
    web.run_app(app, host='0.0.0.0', port=8041)