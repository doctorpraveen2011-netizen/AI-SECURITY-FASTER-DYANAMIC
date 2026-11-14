from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import Conversation, Message

class ConversationManager:
    @staticmethod
    def get_or_create_conversation(
        db: Session,
        conversation_id: Optional[str] = None,
        provider: str = "claude",
        model_name: str = "claude-3-5-sonnet-20241022",
        system_prompt: Optional[str] = None,
        title: str = "New Security Conversation"
    ) -> Conversation:
        if conversation_id:
            conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conv:
                return conv
        
        new_conv = Conversation(
            provider=provider,
            model_name=model_name,
            system_prompt=system_prompt,
            title=title
        )
        db.add(new_conv)
        db.commit()
        db.refresh(new_conv)
        return new_conv

    @staticmethod
    def add_message(
        db: Session,
        conversation_id: str,
        role: str,
        content: str,
        provider: Optional[str] = None,
        model_name: Optional[str] = None,
        tokens_used: int = 0,
        latency_ms: float = 0.0,
        rag_sources: Optional[List[Dict[str, Any]]] = None,
        guardrail_flagged: bool = False
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            provider=provider,
            model_name=model_name,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
            rag_sources=rag_sources,
            guardrail_flagged=guardrail_flagged
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return msg

    @staticmethod
    def get_conversation_history(db: Session, conversation_id: str) -> List[Dict[str, str]]:
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
        return [{"role": m.role, "content": m.content} for m in messages]
