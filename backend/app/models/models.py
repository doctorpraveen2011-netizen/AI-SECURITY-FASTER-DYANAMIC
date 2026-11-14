import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="security_engineer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelConfig(Base):
    __tablename__ = "model_configs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    provider = Column(String(50), nullable=False) # 'claude' or 'gemini'
    model_name = Column(String(100), nullable=False) # e.g. claude-3-5-sonnet, gemini-1.5-flash
    display_name = Column(String(100), nullable=False)
    api_key_configured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    temperature = Column(Float, default=0.7)
    max_tokens = Column(Integer, default=4096)
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), default="New Security Conversation")
    provider = Column(String(50), default="claude")
    model_name = Column(String(100), default="claude-3-5-sonnet")
    system_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False) # user, assistant, system
    content = Column(Text, nullable=False)
    provider = Column(String(50), nullable=True)
    model_name = Column(String(100), nullable=True)
    tokens_used = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    rag_sources = Column(JSON, nullable=True)
    guardrail_flagged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, default=0)
    chunk_count = Column(Integer, default=0)
    status = Column(String(50), default="indexed")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_id = Column(String(36), ForeignKey("knowledge_documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=True) # vector stored as float array
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("KnowledgeDocument", back_populates="chunks")

class Agent(Base):
    __tablename__ = "agents"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    provider = Column(String(50), default="claude")
    model_name = Column(String(100), default="claude-3-5-sonnet")
    system_prompt = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    tools = relationship("AgentTool", back_populates="agent")

class AgentTool(Base):
    __tablename__ = "agent_tools"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_id = Column(String(36), ForeignKey("agents.id"), nullable=True)
    name = Column(String(100), nullable=False) # file_read, email, http_call, mcp_tools
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_enabled = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)
    permission_policy = Column(JSON, nullable=True) # allowlist rules

    agent = relationship("Agent", back_populates="tools")

class AgentExecution(Base):
    __tablename__ = "agent_executions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    task_input = Column(Text, nullable=False)
    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    status = Column(String(50), default="running") # running, completed, waiting_approval, blocked, failed
    steps = Column(JSON, default=list) # trace of thought, tool calls, results
    result = Column(Text, nullable=True)
    security_alerts = Column(JSON, default=list)
    pending_tool_call = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class RiskCategory(Base):
    __tablename__ = "risk_categories"
    id = Column(String(50), primary_key=True) # e.g. LLM01, ASI01
    framework = Column(String(50), nullable=False) # OWASP LLM 2026 or OWASP ASI 2026
    name = Column(String(255), nullable=False) # Prompt Injection
    description = Column(Text, nullable=True)
    severity_level = Column(String(20), default="HIGH")

    test_cases = relationship("AttackTestCase", back_populates="risk_category")

class AttackTestCase(Base):
    __tablename__ = "attack_test_cases"
    id = Column(String(50), primary_key=True) # e.g. TC-LLM01-01
    risk_id = Column(String(50), ForeignKey("risk_categories.id"), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    attack_prompt = Column(Text, nullable=False)
    expected_safe_behavior = Column(Text, nullable=False)
    vulnerability_trigger_pattern = Column(Text, nullable=False)
    severity = Column(String(20), default="HIGH")
    created_at = Column(DateTime, default=datetime.utcnow)

    risk_category = relationship("RiskCategory", back_populates="test_cases")
    executions = relationship("TestExecution", back_populates="test_case")

class AttackCampaign(Base):
    __tablename__ = "attack_campaigns"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    target_provider = Column(String(50), nullable=False) # claude, gemini, or both
    status = Column(String(50), default="pending") # pending, running, completed, cancelled
    total_tests = Column(Integer, default=0)
    completed_tests = Column(Integer, default=0)
    vulnerabilities_found = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    executions = relationship("TestExecution", back_populates="campaign")

class TestExecution(Base):
    __tablename__ = "test_executions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    campaign_id = Column(String(36), ForeignKey("attack_campaigns.id"), nullable=True)
    test_case_id = Column(String(50), ForeignKey("attack_test_cases.id"), nullable=False)
    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    prompt_payload = Column(Text, nullable=False)
    raw_response = Column(Text, nullable=True)
    observed_behavior = Column(Text, nullable=True)
    result = Column(String(20), nullable=False) # VULNERABLE, SAFE, BLOCKED, ERROR
    severity = Column(String(20), default="HIGH")
    evidence = Column(JSON, nullable=True)
    latency_ms = Column(Float, default=0.0)
    executed_at = Column(DateTime, default=datetime.utcnow)

    test_case = relationship("AttackTestCase", back_populates="executions")
    campaign = relationship("AttackCampaign", back_populates="executions")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    risk_id = Column(String(50), nullable=False)
    test_case_id = Column(String(50), nullable=False)
    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    severity = Column(String(20), default="HIGH")
    status = Column(String(50), default="OPEN") # OPEN, MITIGATED, RETEST_PENDING
    evidence_text = Column(Text, nullable=True)
    found_at = Column(DateTime, default=datetime.utcnow)
    mitigated_at = Column(DateTime, nullable=True)

class Mitigation(Base):
    __tablename__ = "mitigations"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    risk_id = Column(String(50), nullable=False)
    defense_type = Column(String(100), nullable=False) # input_filter, output_filter, tool_whitelist, ssrf_guard
    is_active = Column(Boolean, default=True)
    before_risk_pct = Column(Float, default=85.0)
    after_risk_pct = Column(Float, default=12.0)
    description = Column(Text, nullable=True)
    verification_status = Column(String(50), default="VERIFIED") # VERIFIED, PENDING, FAILED
    updated_at = Column(DateTime, default=datetime.utcnow)

class RetestResult(Base):
    __tablename__ = "retest_results"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    vulnerability_id = Column(String(36), nullable=False)
    mitigation_id = Column(String(36), nullable=False)
    retest_payload = Column(Text, nullable=False)
    before_response = Column(Text, nullable=True)
    after_response = Column(Text, nullable=True)
    is_verified = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class MCPConnection(Base):
    __tablename__ = "mcp_connections"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    server_name = Column(String(100), nullable=False)
    server_url = Column(String(255), nullable=False)
    status = Column(String(50), default="CONNECTED") # CONNECTED, BLOCKED, DISCONNECTED
    risk_score = Column(Float, default=11.0)
    discovered_tools = Column(JSON, default=list)
    permissions = Column(JSON, default=dict)
    last_checked = Column(DateTime, default=datetime.utcnow)

class MCPEvent(Base):
    __tablename__ = "mcp_events"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_type = Column(String(100), nullable=False) # PATH_TRAVERSAL_BLOCKED, TOOL_INVOCATION
    details = Column(Text, nullable=False)
    status = Column(String(50), default="BLOCKED")
    created_at = Column(DateTime, default=datetime.utcnow)

class WazuhAlert(Base):
    __tablename__ = "wazuh_alerts"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    rule_id = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    level = Column(Integer, default=7)
    agent_name = Column(String(100), default="ai-security-soc")
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_data = Column(JSON, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    action = Column(String(100), nullable=False)
    actor = Column(String(100), default="security_engineer")
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(100), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.utcnow)
