from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Auth & User
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: str = "security_engineer"

# LLM Providers
class ChatMessage(BaseModel):
    role: str # user, assistant, system
    content: str
    tokens: Optional[int] = 0
    latency_ms: Optional[float] = 0.0

class ChatRequest(BaseModel):
    provider: str = "claude" # claude or gemini
    model_name: Optional[str] = None
    system_prompt: Optional[str] = "You are a secure, ethical AI assistant."
    messages: List[ChatMessage]
    stream: bool = False
    use_rag: bool = False
    apply_guardrails: bool = True
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    provider: str
    model_name: str
    response: str
    tokens_used: int
    latency_ms: float
    rag_sources: Optional[List[Dict[str, Any]]] = None
    guardrail_flagged: bool = False
    guardrail_details: Optional[Dict[str, Any]] = None

class SideBySideRequest(BaseModel):
    prompt: str
    claude_model: str = "claude-3-5-sonnet-20241022"
    gemini_model: str = "gemini-1.5-flash"
    system_prompt: Optional[str] = None

class SideBySideResponse(BaseModel):
    claude_result: ChatResponse
    gemini_result: ChatResponse
    comparison_summary: str

# RAG & Documents
class DocumentChunkInfo(BaseModel):
    chunk_index: int
    content: str

class DocumentInfo(BaseModel):
    id: str
    filename: str
    file_type: str
    file_size: int
    chunk_count: int
    status: str
    created_at: datetime

# Agent
class AgentExecutionRequest(BaseModel):
    task: str
    provider: str = "claude"
    model_name: Optional[str] = None
    enabled_tools: List[str] = ["file_read", "email", "http_call", "mcp_tools"]
    auto_approve_sensitive: bool = False

class AgentApprovalRequest(BaseModel):
    execution_id: str
    action: str # approve or reject
    rejection_reason: Optional[str] = None

class AgentStep(BaseModel):
    step_number: int
    thought: str
    tool: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[Any] = None
    is_sensitive: bool = False
    approval_status: Optional[str] = None

# Red Team
class TestCaseSummary(BaseModel):
    id: str
    risk_id: str
    title: str
    category: str
    severity: str

class CampaignRunRequest(BaseModel):
    name: str = "OWASP 2026 Comprehensive AI Red Team Campaign"
    target_provider: str = "both" # claude, gemini, or both
    risk_ids: Optional[List[str]] = None # None means all 10 risks

class SingleTestRunRequest(BaseModel):
    test_case_id: str
    provider: str = "claude"
    model_name: Optional[str] = None

class TestExecutionResult(BaseModel):
    id: str
    test_case_id: str
    risk_id: str
    provider: str
    model_name: str
    result: str # VULNERABLE, SAFE, BLOCKED
    severity: str
    raw_response: str
    observed_behavior: str
    latency_ms: float
    executed_at: datetime

# Blue Team Mitigations
class MitigationToggleRequest(BaseModel):
    mitigation_id: str
    is_active: bool

class RetestRequest(BaseModel):
    vulnerability_id: str
    mitigation_id: str

# MCP
class MCPToolExecuteRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class MCPPoCRunRequest(BaseModel):
    poc_type: str = "path_traversal" # path_traversal, unauthorized_tool, tool_poisoning
