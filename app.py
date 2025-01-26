import os
from fastapi import FastAPI, HTTPException
import requests
import json

app = FastAPI()

AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")
if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN environment variable is not set")

# We'll add more code here soon!
@app.post("/run")
async def run_task(task: str):
    try:
        # We'll add task handling logic here later
        return {"message": "Task completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    try:
        with open(path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
def handle_task(task: str):
    # This is where we'll use the LLM to understand and execute tasks
    llm_response = call_llm(task)
    # Parse the LLM response and execute the task
    # For now, let's just return a dummy response
    return "Task executed: " + task

def call_llm(prompt: str):
    url = "https://api.aiproxy.io/v1/completions"
    headers = {
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["text"]

# Update the run_task function to use handle_task
@app.post("/run")
async def run_task(task: str):
    try:
        result = handle_task(task)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

