from typing import List

from fastapi import APIRouter
from models.vocabulary import EntityType, RelationType

router = APIRouter(prefix="/api/v1/vocabulary", tags=["vocabulary"])


@router.get("/entity-types", response_model=List[str], tags=["vocabulary"])
def list_entity_types():
    return [e.value for e in EntityType]


@router.get("/relation-types", response_model=List[str], tags=["vocabulary"])
def list_relation_types():
    return [r.value for r in RelationType]
