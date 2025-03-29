from celery import Celery
from app.core.config import settings
from app.database import db
from datetime import datetime
from app.services.pipeline import execute_workflow

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    broker_connection_retry_on_startup=True
)

@celery.task(bind=True)
def execute_workflow_task(self, workflow_params: dict):
    task_id = self.request.id
    
    try:
        # Update status to STARTED
        db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "STARTED", "started_at": datetime.utcnow()}}
        )
        
        # Execute actual workflow
        result = execute_workflow(**workflow_params)
        
        # Store successful result
        db.tasks.update_one(
            {"_id": task_id},
            {"$set": {
                "status": "COMPLETED",
                "completed_at": datetime.utcnow(),
                "result": result
            }}
        )
        return result
        
    except Exception as e:
        db.tasks.update_one(
            {"_id": task_id},
            {"$set": {
                "status": "FAILED",
                "error": str(e),
                "completed_at": datetime.utcnow()
            }}
        )
        raise