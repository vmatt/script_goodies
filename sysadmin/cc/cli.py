import asyncio
import ssl
import websockets
import time
import sys
from io import StringIO
import requests
import json
async def send_message():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    while True:
        try:
            async with websockets.connect('wss://localhost:8000/ws', ssl=ssl_context) as websocket:
                while True:
                    message = await websocket.recv()
                    if message == "helo":
                        print("Connection established")
                        continue
                    message_json = json.loads(message)
                    content = message_json.get("content")
                    loc = {}
                    try:
                        exec(content, globals(), loc)
                    except Exception as e:
                        loc = e
                    requests.post('https://localhost:8000/response',
                                  json.dumps({"text": str(loc)}),
                                  verify='server.crt')
        except Exception as e:
            print(f"Connection to server closed: {e}")
            print("Attempting to reconnect in 5 seconds...")
            time.sleep(5)

asyncio.get_event_loop().run_until_complete(send_message())

