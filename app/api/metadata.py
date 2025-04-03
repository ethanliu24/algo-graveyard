from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..config import get_metadata_service
from ..managers.metadata_manager import MetadataManager

router = APIRouter(
    prefix="/metadata",
    tags=["metadata"]
)

@router.get("", status_code=status.HTTP_200_OK)
def get_all_metadata(metadata_service: Annotated[MetadataManager, Depends(get_metadata_service)]):
    return metadata_service.get_all_metadata()
