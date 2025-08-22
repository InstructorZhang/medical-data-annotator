from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session, create_engine


DB_URL = "sqlite:///annotation.db"
engine = create_engine(DB_URL, echo=False)


def utcnow() -> datetime:
    """Get the current UTC time."""
    return datetime.now(timezone.utc)


def get_session():
    with Session(engine) as session:
        yield session


def ensure_entity_within_doc(entity, doc):
    """Ensure that entity's start/end indices are within bounds of the document text."""
    n = len(doc.text)
    if entity.start < 0 or entity.end > n:
        raise HTTPException(
            status_code=400,
            detail=f"Entity span [{entity.start}, {entity.end}) outside document length {n}.",
        )


def snippet(text: str, start: int, end: int, radius: int = 30) -> str:
    """Generate a text snippet with the specified start and end indices highlighted."""
    start_context = max(0, start - radius)
    end_context = min(len(text), end + radius)
    return (
        text[start_context:start] + "[" + text[start:end] + "]" + text[end:end_context]
    )


def paginate(query, page: int, page_size: int):
    """Apply pagination to a SQLAlchemy query."""
    return query.offset((page - 1) * page_size).limit(page_size)
