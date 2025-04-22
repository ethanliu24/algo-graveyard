from fastapi import APIRouter, Depends, Query, status
from typing import Annotated, Any
from ..config import get_metadata_service
from ..managers.metadata_manager import MetadataManager

router = APIRouter(
    prefix="/metadata",
    tags=["metadata"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_metadata(
    metadata_service: Annotated[MetadataManager, Depends(get_metadata_service)],
    sources: Annotated[bool | None, Query] = None,
    difficulties: Annotated[bool | None, Query] = None,
    statuses: Annotated[bool | None, Query] = None,
    tags: Annotated[bool | None, Query] = None,
    languages: Annotated[bool | None, Query] = None,
    sort_by: Annotated[bool | None, Query] = None,
    order: Annotated[bool | None, Query] = None,
) -> dict[str, list[Any]]:
    return metadata_service.get_metadata(sources, difficulties, statuses, tags, languages, sort_by, order)
