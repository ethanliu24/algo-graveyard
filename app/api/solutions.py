from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Annotated
from pydantic import ValidationError
from ..config import get_solution_service, auth_user_jwt
from ..exceptions.entity_not_found import EntityNotFoundError
from ..managers.solution_manager import SolutionManager
from ..schemas.solution import Solution, SolutionCreate

router = APIRouter(
    prefix="/questions/{question_id}/solutions",
    tags=["solutions"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_solutions(
    question_id: str,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> list[Solution]:
    try:
        return await solution_service.get_all_solutions(question_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{solution_id}", status_code=status.HTTP_200_OK)
async def get_solution(
    question_id: str,
    solution_id: str,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> Solution:
    try:
        return await solution_service.get_solution(question_id, solution_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def create_solution(
    request: Request,
    question_id: str,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> Solution:
    try:
        solution_data = SolutionCreate(**await request.json())
        print(solution_data)
        return await solution_service.create_solution(question_id=question_id, data=solution_data)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

@router.put("/{solution_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def update_solution(
    question_id: str,
    solution_id: str,
    request: Request,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> Solution:
    try:
        data = await request.json()
        return await solution_service.update_solution(question_id, solution_id, data)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable entity. Check if field exists or its value is accepted by the backend."
        )

@router.delete("/{solution_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_user_jwt)])
async def delete_solution(
    question_id: str,
    solution_id: str,
    solution_service: Annotated[SolutionManager, Depends(get_solution_service)]
) -> None:
    try:
        await solution_service.delete_solution(question_id, solution_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
