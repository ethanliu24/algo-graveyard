import fastapi

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from pydantic import ValidationError
from typing import Annotated
from ..config import get_question_service, auth_user_jwt
from ..exceptions.entity_not_found import EntityNotFoundError
from ..managers.question_manager import QuestionManager
from ..schemas.pagination import Pagination
from ..schemas.question import Question, Source, Difficulty, Status, Tag

router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_questions(
    question_service: Annotated[QuestionManager, Depends(get_question_service)],
    source: Annotated[Source | None, Query()] = None,
    difficulty: Annotated[Difficulty | None, Query()] = None,
    status: Annotated[Status | None, Query()] = None,
    tags: Annotated[list[Tag] | None, Query()] = None,
    search: Annotated[str | None, Query()] = None,
    sort_by: Annotated[str | None, Query()] = None,
    order: Annotated[str | None, Query()] = None,
    page: Annotated[int | None, Query()] = None,
    per_page: Annotated[int | None, Query()] = None,
) -> Pagination:
    try:
        return await question_service.get_all_questions(
            source=source,
            difficulty=difficulty,
            status=status,  # note: fastapi also has a status. if using that, do fastapi.status
            tags=tags,
            search=search,
            sort_by=sort_by,
            order=order,
            page=page,
            per_page=per_page,
        )
    except ValueError as e:
        raise HTTPException(status_code=fastapi.status.HTTP_400_BAD_REQUEST, detail=str(e))

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
    request: Request,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> None:
    try:
        question_data = await request.json()
        return await question_service.create_question(data=question_data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{question_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def update_question(
    question_id: str,
    request: Request,
    question_service: Annotated[QuestionManager, Depends(get_question_service)]
) -> Question:
    try:
        data = await request.json()
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
