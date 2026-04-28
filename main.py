from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

app = FastAPI()

FILE = "task.json"

def load_tasks():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=4)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "server running",
            "FILE" : tasks
            }

@app.get("/tasks")
def get_tasks():
    return load_tasks()

@app.get("/recent")
def get_recent():
    tasks = load_tasks()
    return tasks[-5:]

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        data = await ws.receive_text()

        try:
            payload = json.loads(data)
        except:
            payload = {
                "type": "session",
                "task": data,
                "done": False
            }

        payload["timestamp"] = str(datetime.now())

        tasks = load_tasks()
        tasks.append(payload)
        save_tasks(tasks)

        await ws.send_text("saved")

@app.post("/ai-log")
def ai_log(data: dict):
    data["timestamp"] = str(datetime.now())
    tasks = load_tasks()
    tasks.append(data)
    save_tasks(tasks)
    return {"status": "logged"}

@app.post("/tasks")
def add_task(task: dict):
    task["timestamp"] = str(datetime.now())
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return {"message": "saved", "data": task}
