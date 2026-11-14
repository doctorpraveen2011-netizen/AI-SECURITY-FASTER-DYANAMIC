import uuid
import time
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.schemas import ChatRequest, ChatResponse, SideBySideRequest, SideBySideResponse
from app.llm.llm_router import llm_router
from app.llm.model_registry import MODELS_REGISTRY, get_models_by_provider
from app.llm.conversation_manager import ConversationManager
from app.rag.vector_store import VectorStore
from app.blueteam.guardrails import InputGuardrail, OutputGuardrail
from app.models.models import Conversation, Message

router = APIRouter(prefix="/llm", tags=["LLM Engine"])

@router.get("/models")
def list_models():
    return list(MODELS_REGISTRY.values())

@router.get("/status")
async def check_status():
    return await llm_router.get_all_provider_status()

@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    # 1. Conversation tracking
    conv = ConversationManager.get_or_create_conversation(
        db=db,
        conversation_id=request.conversation_id,
        provider=request.provider,
        model_name=request.model_name or "claude-3-5-sonnet-20241022",
        system_prompt=request.system_prompt
    )

    last_user_msg = request.messages[-1].content if request.messages else ""
    guardrail_flagged = False
    guardrail_details = None

    # 2. Input Guardrail Inspection (if enabled)
    if request.apply_guardrails:
        is_blocked, blocked_msg, detected = InputGuardrail.inspect_input(last_user_msg)
        if is_blocked:
            latency = (time.time() - start_time) * 1000
            # Record in conversation
            ConversationManager.add_message(
                db, conv.id, "user", last_user_msg, request.provider, request.model_name
            )
            ConversationManager.add_message(
                db, conv.id, "assistant", blocked_msg, request.provider, request.model_name,
                tokens_used=15, latency_ms=latency, guardrail_flagged=True
            )
            return ChatResponse(
                id=str(uuid.uuid4()),
                provider=request.provider,
                model_name=request.model_name or "guardrail",
                response=blocked_msg,
                tokens_used=15,
                latency_ms=round(latency, 2),
                guardrail_flagged=True,
                guardrail_details={"detected_threats": detected}
            )

    # 3. RAG Retrieval (if requested)
    rag_sources = None
    system_prompt = request.system_prompt or "You are a secure, ethical enterprise cybersecurity assistant."
    if request.use_rag and last_user_msg:
        rag_context, sources = VectorStore.format_context_for_prompt(db, last_user_msg)
        if rag_context:
            system_prompt = f"{system_prompt}\n{rag_context}"
            rag_sources = sources

    # 4. Message conversion
    formatted_messages = [{"role": m.role, "content": m.content} for m in request.messages]

    # 5. Invoke LLM Provider
    result = await llm_router.generate_completion(
        provider=request.provider,
        messages=formatted_messages,
        model_name=request.model_name,
        system_prompt=system_prompt
    )

    raw_response = result.get("content", "")

    # 6. Output Guardrail (Redact secrets/PII)
    if request.apply_guardrails:
        was_redacted, sanitized_text, redactions = OutputGuardrail.inspect_and_sanitize(raw_response)
        if was_redacted:
            raw_response = sanitized_text
            guardrail_flagged = True
            guardrail_details = {"redactions": redactions}

    latency = (time.time() - start_time) * 1000

    # 7. Persist messages in database
    ConversationManager.add_message(
        db, conv.id, "user", last_user_msg, request.provider, result.get("model_name")
    )
    assistant_msg = ConversationManager.add_message(
        db, conv.id, "assistant", raw_response, request.provider, result.get("model_name"),
        tokens_used=result.get("tokens_used", 50),
        latency_ms=round(latency, 2),
        rag_sources=rag_sources,
        guardrail_flagged=guardrail_flagged
    )

    return ChatResponse(
        id=assistant_msg.id,
        provider=request.provider,
        model_name=result.get("model_name", request.model_name or "model"),
        response=raw_response,
        tokens_used=result.get("tokens_used", 50),
        latency_ms=round(latency, 2),
        rag_sources=rag_sources,
        guardrail_flagged=guardrail_flagged,
        guardrail_details=guardrail_details
    )

@router.post("/compare", response_model=SideBySideResponse)
async def side_by_side_compare(request: SideBySideRequest):
    res = await llm_router.side_by_side_comparison(
        prompt=request.prompt,
        claude_model=request.claude_model,
        gemini_model=request.gemini_model,
        system_prompt=request.system_prompt
    )

    claude_data = res["claude"]
    gemini_data = res["gemini"]

    summary = f"Claude completed in {claude_data['latency_ms']}ms ({claude_data['tokens_used']} tokens). Gemini completed in {gemini_data['latency_ms']}ms ({gemini_data['tokens_used']} tokens). Delta: {res['latency_delta_ms']}ms."

    return SideBySideResponse(
        claude_result=ChatResponse(
            id=str(uuid.uuid4()),
            provider="claude",
            model_name=claude_data.get("model_name", request.claude_model),
            response=claude_data.get("content", ""),
            tokens_used=claude_data.get("tokens_used", 0),
            latency_ms=claude_data.get("latency_ms", 0.0)
        ),
        gemini_result=ChatResponse(
            id=str(uuid.uuid4()),
            provider="gemini",
            model_name=gemini_data.get("model_name", request.gemini_model),
            response=gemini_data.get("content", ""),
            tokens_used=gemini_data.get("tokens_used", 0),
            latency_ms=gemini_data.get("latency_ms", 0.0)
        ),
        comparison_summary=summary
    )

@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    return [{
        "id": c.id,
        "title": c.title,
        "provider": c.provider,
        "model_name": c.model_name,
        "message_count": len(c.messages),
        "updated_at": c.updated_at.isoformat()
    } for c in convs]

@router.get("/conversations/{conversation_id}")
def get_conversation_detail(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "id": conv.id,
        "title": conv.title,
        "provider": conv.provider,
        "model_name": conv.model_name,
        "system_prompt": conv.system_prompt,
        "messages": [{
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "tokens_used": m.tokens_used,
            "latency_ms": m.latency_ms,
            "rag_sources": m.rag_sources,
            "guardrail_flagged": m.guardrail_flagged,
            "created_at": m.created_at.isoformat()
        } for m in conv.messages]
    }
