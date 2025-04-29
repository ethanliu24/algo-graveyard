from fastapi import APIRouter
from .api import auth, metadata, questions, solutions, export

api_router = APIRouter(prefix="/api")
api_router.include_router(questions.router)
api_router.include_router(solutions.router)
api_router.include_router(auth.router)
api_router.include_router(metadata.router)
api_router.include_router(export.router)
