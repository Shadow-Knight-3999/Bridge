import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:8000/ws")

print("Connected")

while True:
    text = input("Enter update: ")

    payload = {
        "type": "session",
        "task": text,
        "done": False
    }

    ws.send(json.dumps(payload))

    res = ws.recv()
    print("Server:", res)
