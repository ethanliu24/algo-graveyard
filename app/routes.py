from fastapi import APIRouter
from .api import questions, solutions

api_router = APIRouter(prefix="/api")
api_router.include_router(questions.router)
api_router.include_router(solutions.router)
