from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from ..config import get_question_service
from ..managers.question_manager import QuestionManager
from ..schemas.question import Question

router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_questions(
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> list[Question]:  # TODO add filter
    return await question_service.get_all_questions()

@router.get("/{question_id}", status_code=status.HTTP_200_OK)
async def get_question(
    question_id: str,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> Question:
    try:
        return await question_service.get_question(question_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
