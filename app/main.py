from fastapi import FastAPI
from app.endpoints import router as workflow_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Product Management Assistant",
    description="API for processing tweets and creating Trello cards",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflow_router, prefix="/api/v1")