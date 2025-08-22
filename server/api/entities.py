from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from models.database import Document, Entity, Relation
from models.schema import EntityCreate, EntityRead
from server.utils.utils import get_session, ensure_entity_within_doc, snippet

router = APIRouter(prefix="/api/v1", tags=["entities"])


@router.post("/documents/{doc_id}/entities", response_model=EntityRead, tags=["entities"])
def create_entity(
    doc_id: int, payload: EntityCreate, session: Session = Depends(get_session)
):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    ensure_entity_within_doc(payload, doc)
    ent = Entity(
        document_id=doc_id,
        id=payload.id,
        start=payload.start,
        end=payload.end,
        label=payload.label,
        code_system=payload.code_system,
        code=payload.code,
        annotator=payload.annotator,
    )
    session.add(ent)
    session.commit()
    session.refresh(ent)
    return EntityRead(
        **ent.dict(),
        text_snippet=snippet(doc.text, ent.start, ent.end),
    )


@router.get(
    "/documents/{doc_id}/entities", response_model=List[EntityRead], tags=["entities"]
)
def list_entities(doc_id: int, session: Session = Depends(get_session)):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    stmt = (
        select(Entity).where(Entity.document_id == doc_id).order_by(Entity.start.asc())
    )
    entities = session.exec(stmt).all()
    out = [
        EntityRead(
            **e.dict(),
            text_snippet=snippet(doc.text, e.start, e.end),
        )
        for e in entities
    ]
    return out


@router.delete("/entities/{entity_id}", status_code=204, tags=["entities"])
def delete_entity(entity_id: int, session: Session = Depends(get_session)):
    ent = session.get(Entity, entity_id)
    if not ent:
        raise HTTPException(404, detail="Entity not found")
    # Also delete relations that reference this entity
    rel_stmt = select(Relation).where(
        (Relation.source_entity_id == entity_id)
        | (Relation.target_entity_id == entity_id)
    )
    for rel in session.exec(rel_stmt).all():
        session.delete(rel)
    session.delete(ent)
    session.commit()
    return
