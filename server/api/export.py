import json
from typing import List

from fastapi import APIRouter, Depends
from fastapi.params import Body
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from models.database import Document, Entity, Relation
from models.schema import ExportQuery, ExportDocument, ExportEntity, ExportRelation
from server.utils.utils import get_session

router = APIRouter(prefix="/api/v1", tags=["export"])


def _serialize_export_doc(doc: Document, session: Session) -> ExportDocument:
    ents = session.exec(
        select(Entity).where(Entity.document_id == doc.id).order_by(Entity.start.asc())
    ).all()
    rels = session.exec(select(Relation).where(Relation.document_id == doc.id)).all()
    return ExportDocument(
        document_id=doc.id,
        external_id=doc.external_id,
        text=doc.text,
        status=doc.status,
        entities=[
            ExportEntity(
                id=e.id,
                start=e.start,
                end=e.end,
                label=e.label,
                code_system=e.code_system,
                code=e.code,
                annotator=e.annotator,
                created_at=e.created_at,
            )
            for e in ents
        ],
        relations=[
            ExportRelation(
                id=r.id,
                source_entity_id=r.source_entity_id,
                target_entity_id=r.target_entity_id,
                predicate=r.predicate,
                annotator=r.annotator,
                created_at=r.created_at,
            )
            for r in rels
        ],
    )


@router.post("/export", tags=["export"])
async def export_annotations(
    query: ExportQuery = Body(default_factory=ExportQuery),
    session: Session = Depends(get_session),
):
    stmt = select(Document)
    if query.document_ids:
        stmt = stmt.where(Document.id.in_(query.document_ids))
    if query.status:
        stmt = stmt.where(Document.status == query.status)
    docs = session.exec(stmt).all()

    def generate_jsonl():
        for doc in docs:
            payload = _serialize_export_doc(doc, session)
            yield json.dumps(payload.model_dump(), default=str, ensure_ascii=False) + "\n"

    headers = {"Content-Disposition": "attachment; filename=annotations.jsonl"}
    return StreamingResponse(
        generate_jsonl(), media_type="application/x-ndjson", headers=headers
    )
