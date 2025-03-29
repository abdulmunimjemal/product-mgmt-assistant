from fastapi import APIRouter
from app.services.pipeline import execute_workflow
from app.models import WorkflowRequest, WorkflowResponse

router = APIRouter()

@router.post("/execute-workflow", response_model=WorkflowResponse)
def trigger_workflow(request: WorkflowRequest):
    """Endpoint to execute the tweet processing workflow"""
    return execute_workflow(
        product_name=request.product_name,
        product_description=request.product_description,
        trello_api_key=request.trello_api_key,
        trello_token=request.trello_token,
        prioritization_rule=request.prioritization_rule,
        time_period=request.time_period,
        max_tweets=request.max_tweets,
        board_id=request.board_id,
        board_name=request.board_name,
        list_name=request.list_name
    )