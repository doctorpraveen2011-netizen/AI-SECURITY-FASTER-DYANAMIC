import math
import hashlib
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.models import DocumentChunk, KnowledgeDocument

class VectorStore:
    @staticmethod
    def get_embedding(text: str, dim: int = 128) -> List[float]:
        """
        Generates a deterministic semantic pseudo-embedding vector for text similarity.
        Normalizes token hashing across the dimension vector.
        """
        vec = [0.0] * dim
        words = text.lower().split()
        for idx, word in enumerate(words):
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            pos = h % dim
            val = (h % 1000) / 1000.0 - 0.5
            vec[pos] += val
        
        # Normalize to unit length
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(0.0, min(1.0, dot))

    @classmethod
    def search(cls, db: Session, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        q_emb = cls.get_embedding(query)
        chunks = db.query(DocumentChunk).all()
        if not chunks:
            return []

        scored_chunks: List[Tuple[float, DocumentChunk]] = []
        for c in chunks:
            if c.embedding:
                score = cls.cosine_similarity(q_emb, c.embedding)
            else:
                # Direct term frequency overlap
                q_words = set(query.lower().split())
                c_words = set(c.content.lower().split())
                overlap = len(q_words.intersection(c_words))
                score = overlap / (len(q_words) + 1)
            scored_chunks.append((score, c))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, chunk in scored_chunks[:top_k]:
            doc = db.query(KnowledgeDocument).filter(KnowledgeDocument.id == chunk.document_id).first()
            results.append({
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "document_name": doc.filename if doc else "Internal Enterprise Document",
                "content": chunk.content,
                "similarity_score": round(score, 3)
            })
        return results

    @classmethod
    def format_context_for_prompt(cls, db: Session, query: str) -> Tuple[str, List[Dict[str, Any]]]:
        sources = cls.search(db, query, top_k=2)
        if not sources:
            return "", []
        
        context_text = "\n\n--- ENTERPRISE KNOWLEDGE BASE RETRIEVAL ---\n"
        for idx, s in enumerate(sources):
            context_text += f"[Source {idx+1}: {s['document_name']} (Relevance: {s['similarity_score']})]\n{s['content']}\n\n"
        context_text += "--- END RETRIEVED CONTEXT ---\n"
        return context_text, sources
