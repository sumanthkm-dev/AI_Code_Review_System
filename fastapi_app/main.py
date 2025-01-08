from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import httpx

app = FastAPI()


class AnalysePRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None


@app.post("/start_task")
async def start_task_endpoint(task_request: AnalysePRRequest):
    data = {
        "repo_url": task_request.repo_url,
        "pr_number": task_request.pr_number,
        "github_token": task_request.github_token,
    }
    async with httpx.AsyncClient as client:
        response = await client.post("http://localhost:8000/start_task", data=data)
        if response.status != 200:
            return {"error": "Something went wrong", "details": response.text}
    task_id = response.json().get("task_id")
    return {"task_id": task_id, "status": "Task Started"}


@app.get("/check_task_status/{task_id}/")
async def check_task_status(task_id: str):
    async with httpx.AsyncClient as client:
        response = await client.get(
            f"http://localhost:8000/check_task_status/{task_id}",
        )
        return response.json()
    return {"message": "Something went wrong"}
