from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.database import db
from app.tasks.workflow_tasks import execute_workflow_task
from app.models import WorkflowRequest, TaskResponse
import uuid

router = APIRouter()

@router.post("/workflows", response_model=TaskResponse)
async def create_workflow(request: WorkflowRequest):
    task_id = str(uuid.uuid4())
    
    # Create initial task document
    db.tasks.insert_one({
        "_id": task_id,
        "status": "PENDING",
        "params": request.dict(),
        "created_at": datetime.utcnow()
    })
    
    # Start Celery task
    execute_workflow_task.apply_async(
        args=[request.dict()],
        task_id=task_id
    )
    
    return {"task_id": task_id, "status": "PENDING"}

@router.get("/workflows/{task_id}", response_model=TaskResponse)
async def get_workflow_status(task_id: str):
    task = db.tasks.find_one({"_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["_id"] = str(task["_id"])
    task["task_id"] = task.pop("_id")
    return task