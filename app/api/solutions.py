from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from typing import Annotated
from ..config import get_solution_service
from ..managers.solution_manager import SolutionManager
from ..schemas.solution import Solution, SolutionCreate

router = APIRouter(
    prefix="/questions/{question_id}/solutions",
    tags=["solutions"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_questions(
    question_id: str,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> list[Solution]:
    return await solution_service.get_all_solutions(question_id)

@router.get("/{solution_id}", status_code=status.HTTP_200_OK)
async def get_question(
    question_id: str,
    solution_id: str,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> Solution:
    try:
        return await solution_service.get_solution(question_id, solution_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("")
async def create_question(
    question_id: str,
    solution_data: SolutionCreate,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> str:
    return await solution_service.create_solution(data=solution_data)

