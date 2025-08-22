from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator
from .vocabulary import EntityType, RelationType


# -----------------------------
# Pydantic Schemas (I/O Models)
# -----------------------------


class DocumentCreate(BaseModel):
    id: int
    text: str
    external_id: Optional[str] = None
    status: Optional[str] = Field(default="unannotated")


class DocumentRead(BaseModel):
    id: int
    external_id: Optional[str]
    text: str
    status: str
    created_at: datetime
    updated_at: datetime


class DocumentUpdate(BaseModel):
    text: Optional[str] = None
    status: Optional[str] = None


class EntityCreate(BaseModel):
    id: Optional[int] = None
    start: int
    end: int
    label: EntityType
    code_system: Optional[str] = None
    code: Optional[str] = None
    annotator: Optional[str] = Field(
        default=None, description="Annotator identifier (e.g., email/username)"
    )

    @validator("end")
    def _end_gt_start(cls, v, values):
        if "start" in values and v <= values["start"]:
            raise ValueError("'end' must be > 'start'")
        return v


class EntityRead(BaseModel):
    id: int
    document_id: int
    start: int
    end: int
    label: EntityType
    code_system: Optional[str]
    code: Optional[str]
    annotator: Optional[str]
    created_at: datetime
    text_snippet: Optional[str] = None


class RelationCreate(BaseModel):
    source_entity_id: int
    target_entity_id: int
    predicate: RelationType
    annotator: Optional[str] = None


class RelationRead(BaseModel):
    id: int
    document_id: int
    source_entity_id: int
    target_entity_id: int
    predicate: RelationType
    annotator: Optional[str]
    created_at: datetime


# Export schemas
class ExportEntity(BaseModel):
    id: int
    start: int
    end: int
    label: EntityType
    code_system: Optional[str]
    code: Optional[str]
    annotator: Optional[str]
    created_at: datetime


class ExportRelation(BaseModel):
    id: int
    source_entity_id: int
    target_entity_id: int
    predicate: RelationType
    annotator: Optional[str]
    created_at: datetime


class ExportDocument(BaseModel):
    document_id: int
    external_id: Optional[str]
    text: str
    status: str
    entities: List[ExportEntity]
    relations: List[ExportRelation]


# -----------------------------
# Export Endpoints
# -----------------------------

class ExportQuery(BaseModel):
    document_ids: Optional[List[int]] = None
    status: Optional[str] = None