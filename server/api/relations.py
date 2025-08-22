from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models.database import Document, Entity, Relation
from models.schema import RelationCreate, RelationRead
from server.utils.utils import get_session


router = APIRouter(prefix="/api/v1", tags=["relations"])


@router.post(
    "/documents/{doc_id}/relations", response_model=RelationRead, tags=["relations"]
)
def create_relation(
    doc_id: int, payload: RelationCreate, session: Session = Depends(get_session)
):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    src = session.get(Entity, payload.source_entity_id)
    tgt = session.get(Entity, payload.target_entity_id)
    if not src or not tgt:
        raise HTTPException(400, detail="Source or target entity does not exist")
    if src.document_id != doc_id or tgt.document_id != doc_id:
        raise HTTPException(
            400, detail="Both entities must belong to the same document"
        )
    rel = Relation(
        document_id=doc_id,
        source_entity_id=payload.source_entity_id,
        target_entity_id=payload.target_entity_id,
        predicate=payload.predicate,
        annotator=payload.annotator,
    )
    session.add(rel)
    session.commit()
    session.refresh(rel)
    return rel


@router.get(
    "/documents/{doc_id}/relations",
    response_model=List[RelationRead],
    tags=["relations"],
)
def list_relations(doc_id: int, session: Session = Depends(get_session)):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    stmt = (
        select(Relation)
        .where(Relation.document_id == doc_id)
        .order_by(Relation.id.asc())
    )
    return session.exec(stmt).all()


@router.delete("/relations/{relation_id}", status_code=204, tags=["relations"])
def delete_relation(relation_id: int, session: Session = Depends(get_session)):
    rel = session.get(Relation, relation_id)
    if not rel:
        raise HTTPException(404, detail="Relation not found")
    session.delete(rel)
    session.commit()
    return
