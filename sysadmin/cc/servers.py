
from helpers import generate_ssl_key
from typing import Dict, List
from fastapi import FastAPI, WebSocket, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn
from starlette.websockets import WebSocketDisconnect
import json
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTPS redirect middleware
app.add_middleware(HTTPSRedirectMiddleware)

# Global exception handler for WebSocketDisconnect
@app.exception_handler(WebSocketDisconnect)
async def websocket_disconnect_exception_handler(request, exc):
    print(f"WebSocketDisconnect: {exc}")
    return None
active_websockets: List[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        await websocket.send_text("helo")

        while True:
            message = await websocket.receive_text()
            print("Message received: " + message)
            await websocket.send_text(f"Message received: {message}")
    except WebSocketDisconnect as e:
        print(f"WebSocketDisconnect: {e}")
        active_websockets.remove(websocket)

@app.post('/response')
async def response(request: Request):
    data = json.loads(await request.body())
    text = data.get('text')
    print(f"Received response: {text}")
    return {'received_text': text}

@app.post("/file")
async def read_file(data: Dict[str, str]):
    file_path = data.get("file_path")
    if file_path is None:
        return {"error": "file_path parameter is missing"}

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}

        # Send content to all active websockets
    data["content"] = content
    for websocket in active_websockets:
        await websocket.send_text(json.dumps(data))

    return {"content": content}
if __name__ == "__main__":
    generate_ssl_key()
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="server.key", ssl_certfile="server.crt")
