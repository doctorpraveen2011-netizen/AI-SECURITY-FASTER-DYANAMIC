import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import KnowledgeDocument, DocumentChunk
from app.rag.document_processor import DocumentProcessor
from app.rag.vector_store import VectorStore
from app.core.config import settings

router = APIRouter(prefix="/rag", tags=["RAG & Knowledge Base"])

@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(KnowledgeDocument).order_by(KnowledgeDocument.created_at.desc()).all()
    return [{
        "id": d.id,
        "filename": d.filename,
        "file_type": d.file_type,
        "file_size": d.file_size,
        "chunk_count": d.chunk_count,
        "status": d.status,
        "description": d.description,
        "created_at": d.created_at.isoformat()
    } for d in docs]

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content_bytes = await file.read()
    filename = file.filename or "uploaded_doc.txt"
    file_type = file.content_type or "text/plain"
    
    text = DocumentProcessor.extract_text(filename, content_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from document.")

    # Save to knowledge base storage
    save_path = settings.KNOWLEDGE_BASE_DIR / filename
    with open(save_path, "wb") as f:
        f.write(content_bytes)

    chunks = DocumentProcessor.chunk_text(text, chunk_size=250, overlap=30)
    
    doc = KnowledgeDocument(
        filename=filename,
        file_type=file_type,
        file_size=len(content_bytes),
        chunk_count=len(chunks),
        description=f"User uploaded document ({len(chunks)} chunks indexed)",
        status="indexed"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    for idx, chunk_text in enumerate(chunks):
        emb = VectorStore.get_embedding(chunk_text)
        chunk = DocumentChunk(
            document_id=doc.id,
            chunk_index=idx,
            content=chunk_text,
            embedding=emb
        )
        db.add(chunk)
    db.commit()

    return {
        "id": doc.id,
        "filename": doc.filename,
        "chunk_count": len(chunks),
        "status": "indexed",
        "message": f"Successfully parsed and indexed {len(chunks)} chunks into vector store."
    }

@router.get("/search")
def search_knowledge_base(query: str, top_k: int = 3, db: Session = Depends(get_db)):
    results = VectorStore.search(db, query, top_k=top_k)
    return {"query": query, "results": results}
