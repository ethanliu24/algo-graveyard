from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from typing import Annotated
from ..config import get_question_service
from ..exceptions.entity_not_found import EntityNotFoundError
from ..managers.question_manager import QuestionManager
from ..schemas.question import Question, QuestionCreate

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
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("")
async def create_question(
    question_data: QuestionCreate,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> Question:
    return await question_service.create_question(data=question_data)

@router.put("/{question_id}")
async def update_question(
    question_id: str,
    data: dict,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> None:
    try:
        await question_service.update_question(data, question_id)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{question_id}")
async def delete_quesiton(
    question_id: str,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> None:
    await question_service.delete_question(question_id)
