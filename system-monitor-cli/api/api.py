from fastapi import FastAPI
import json

app = FastAPI()


def read_logs():
    try:
        with open("logs/system.log") as f:
            lines = f.readlines()[-100:]
        return [json.loads(l) for l in lines]
    except FileNotFoundError:
        return []


@app.get("/metrics")
def metrics():
    return read_logs()
