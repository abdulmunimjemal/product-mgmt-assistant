from pydantic import BaseModel
from typing import Optional

class Metrics(BaseModel):
    time_taken: float
    processed_tweets: int
    cards_added: int
    classification_errors: int
    trello_errors: int

class WorkflowRequest(BaseModel):
    product_name: str
    product_description: str
    trello_api_key: str
    trello_token: str
    prioritization_rule: str
    time_period: str = '1d'
    max_tweets: int = 5
    board_id: Optional[str] = None
    board_name: str = "Product Development"
    list_name: str = "Social Media"

class WorkflowResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    stage: Optional[str] = None
    metrics: Metrics
    message: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: WorkflowResponse | dict | None = None