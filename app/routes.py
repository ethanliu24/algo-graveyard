from fastapi import APIRouter
from .api import questions

api_router = APIRouter(prefix="/api")
api_router.include_router(questions.router)
