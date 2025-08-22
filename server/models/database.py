from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field as SQLField
from sqlmodel import SQLModel
from .vocabulary import EntityType, RelationType

# -----------------------------
# ORM Models (SQLModel)
# -----------------------------


class Document(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    external_id: Optional[str] = SQLField(default=None, index=True)
    text: str
    status: str = SQLField(default="unannotated", index=True)
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))


class Entity(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    document_id: int = SQLField(foreign_key="document.id", index=True)

    start: int
    end: int
    label: EntityType = SQLField(sa_column_kwargs={"nullable": False})
    code_system: Optional[str] = None
    code: Optional[str] = None

    annotator: Optional[str] = None
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))


class Relation(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    document_id: int = SQLField(foreign_key="document.id", index=True)

    source_entity_id: int = SQLField(foreign_key="entity.id")
    target_entity_id: int = SQLField(foreign_key="entity.id")

    predicate: RelationType = SQLField(sa_column_kwargs={"nullable": False})

    annotator: Optional[str] = None
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))
