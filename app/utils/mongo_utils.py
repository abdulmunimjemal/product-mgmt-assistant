from datetime import datetime
from bson import ObjectId

def create_task_record(db, task_id: str):
    task = {
        "_id": task_id,
        "status": "PENDING",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    db.tasks.insert_one(task)
    return task

def update_task_status(db, task_id: str, status: str, result: dict = None):
    update_data = {
        "status": status,
        "updated_at": datetime.utcnow()
    }
    if result:
        update_data["result"] = result
    db.tasks.update_one({"_id": task_id}, {"$set": update_data})