from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import Annotated
from ..config import get_export_service
from ..exceptions.entity_not_found import EntityNotFoundError
from ..managers.export_manager import ExportManager

router = APIRouter(
    prefix="/export",
    tags=["export"]
)

@router.post("/{question_id}", status_code=status.HTTP_200_OK)
async def export_question(
    request: Request,
    question_id: str,
    export_service: Annotated[ExportManager, Depends(get_export_service)]
):
    try:
        solution_ids = (await request.json())["solution_ids"]
        if not isinstance(solution_ids, list) or not all(isinstance(item, str) for item in solution_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="<solution_ids> must be a list of strings.")

        return await export_service.export_question(question_id, solution_ids)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing <solution_ids>' field.")
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
