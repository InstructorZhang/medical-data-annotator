"""
Medical Annotation Backend (FastAPI)
-----------------------------------
FastAPI backend to support:
1) Entity annotations over clinical text
2) Relation annotations between entities
3) Export of annotations for ML pipelines (JSONL)

Tech stack: FastAPI, SQLModel (SQLAlchemy + Pydantic), SQLite.

Run locally:
    uvicorn server.main:app --reload

Environment:
    pip install fastapi uvicorn sqlmodel pydantic-settings python-multipart

Notes:
- Uses SQLite by default: ./annotation.db
- CORS enabled for local dev (http://localhost:3000, http://127.0.0.1:3000)
- Offsets are validated to reside within the document text length
- Relation creation validates entity existence and document consistency
- Timestamps are stored in UTC ISO 8601
- Designed to be paired with a React/TypeScript frontend
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import SQLModel, create_engine
from api import documents, entities, relations, export


DB_URL = "sqlite:///annotation.db"
engine = create_engine(DB_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Medical Annotation Backend", version="1.0.0", lifespan=lifespan)
app.include_router(documents.router)
app.include_router(entities.router)
app.include_router(relations.router)
app.include_router(export.router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["ops"])
def health():
    """Health check endpoint"""
    return {"status": "ok", "version": "1.0.0", "db_url": DB_URL}
