# app/database.py
from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_URI)
db = client[settings.MONGODB_DB_NAME]