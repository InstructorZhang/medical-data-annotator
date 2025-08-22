from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select

from models.database import Document, Entity, Relation
from models.schema import DocumentCreate, DocumentRead, DocumentUpdate
from server.utils.utils import get_session, utcnow, paginate


router = APIRouter(prefix="/api/v1/documents", tags=["documents"])

@router.post("/", response_model=DocumentRead, tags=["documents"])
def create_document(payload: DocumentCreate, session: Session = Depends(get_session)):
    doc = Document(
        text=payload.text,
        id=payload.id,
        external_id=payload.external_id,
        status=payload.status or "unannotated",
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc


@router.get("/{doc_id}", response_model=DocumentRead, tags=["documents"])
def get_document(doc_id: int, session: Session = Depends(get_session)):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    return doc


@router.get("/", response_model=List[DocumentRead], tags=["documents"])
def list_documents(
    status: Optional[str] = Query(default=None),
    q: Optional[str] = Query(
        default=None, description="Full-text LIKE search over content"
    ),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    session: Session = Depends(get_session),
):
    stmt = select(Document)
    if status:
        stmt = stmt.where(Document.status == status)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Document.text.like(like))
    stmt = stmt.order_by(Document.id.desc())
    stmt = paginate(stmt, page, page_size)
    return session.exec(stmt).all()


@router.patch("/{doc_id}", response_model=DocumentRead, tags=["documents"])
def update_document(
    doc_id: int, payload: DocumentUpdate, session: Session = Depends(get_session)
):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    if payload.text is not None:
        doc.text = payload.text
    if payload.status is not None:
        doc.status = payload.status
    doc.updated_at = utcnow()
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc


@router.delete("/{doc_id}", status_code=204, tags=["documents"])
def delete_document(doc_id: int, session: Session = Depends(get_session)):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(404, detail="Document not found")
    # cascade delete relations/entities for this doc
    session.exec(select(Relation).where(Relation.document_id == doc_id)).all()
    session.exec(select(Entity).where(Entity.document_id == doc_id)).all()
    session.delete(doc)
    session.commit()
    return
