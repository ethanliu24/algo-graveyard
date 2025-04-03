from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from typing import Annotated
from ..config import get_question_service, auth_user_jwt
from ..exceptions.entity_not_found import EntityNotFoundError
from ..managers.question_manager import QuestionManager
from ..schemas.question import Question, QuestionCreate, QuestionAll, Source, Difficulty, Status

router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_questions(
    question_service: Annotated[QuestionManager, Depends(get_question_service)],
    source: Source = None,
    difficulty: Difficulty = None,
    q_status: Status = None,
    tags: list[str] = None,
    search: str = None,
    sort_by: str = None,
    order: str = None,
    page: int = None,
    per_page: int = None,
    paginate: bool = None
) -> QuestionAll:
    try:
        return await question_service.get_all_questions(
            source=source,
            difficulty=difficulty,
            status=q_status,
            tags=tags,
            search=search,
            sort_by=sort_by,
            order=order,
            page=page,
            per_page=per_page,
            paginate=paginate
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{question_id}", status_code=status.HTTP_200_OK)
async def get_question(
    question_id: str,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> Question:
    try:
        return await question_service.get_question(question_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def create_question(
    question_data: QuestionCreate,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> Question:
    return await question_service.create_question(data=question_data)

@router.put("/{question_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def update_question(
    question_id: str,
    data: dict,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> Question:
    try:
        return await question_service.update_question(data, question_id)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{question_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def delete_quesiton(
    question_id: str,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> None:
    try:
        await question_service.delete_question(question_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
