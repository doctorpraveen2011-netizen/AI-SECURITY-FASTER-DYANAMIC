const API_BASE = '/api';

export const api = {
  // Dashboard
  getDashboardOverview: async () => {
    const res = await fetch(`${API_BASE}/dashboard/overview`);
    return res.json();
  },
  getDashboardMetrics: async () => {
    const res = await fetch(`${API_BASE}/dashboard/metrics`);
    return res.json();
  },
  getRiskCoverage: async () => {
    const res = await fetch(`${API_BASE}/dashboard/risk-coverage`);
    return res.json();
  },
  getRecentTests: async () => {
    const res = await fetch(`${API_BASE}/dashboard/recent-tests`);
    return res.json();
  },
  getMitigations: async () => {
    const res = await fetch(`${API_BASE}/dashboard/mitigations`);
    return res.json();
  },
  getModelStatus: async () => {
    const res = await fetch(`${API_BASE}/dashboard/model-status`);
    return res.json();
  },
  getIntegrationsStatus: async () => {
    const res = await fetch(`${API_BASE}/dashboard/integrations`);
    return res.json();
  },

  // LLM Chat & Comparison
  listModels: async () => {
    const res = await fetch(`${API_BASE}/llm/models`);
    return res.json();
  },
  sendChat: async (data: {
    provider: string;
    model_name?: string;
    system_prompt?: string;
    messages: Array<{ role: string; content: string }>;
    use_rag?: boolean;
    apply_guardrails?: boolean;
    conversation_id?: string;
  }) => {
    const res = await fetch(`${API_BASE}/llm/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  compareModels: async (data: {
    prompt: string;
    claude_model?: string;
    gemini_model?: string;
    system_prompt?: string;
  }) => {
    const res = await fetch(`${API_BASE}/llm/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  listConversations: async () => {
    const res = await fetch(`${API_BASE}/llm/conversations`);
    return res.json();
  },
  getConversationDetail: async (id: string) => {
    const res = await fetch(`${API_BASE}/llm/conversations/${id}`);
    return res.json();
  },

  // RAG & Knowledge Base
  listDocuments: async () => {
    const res = await fetch(`${API_BASE}/rag/documents`);
    return res.json();
  },
  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/rag/upload`, {
      method: 'POST',
      body: formData,
    });
    return res.json();
  },
  searchKnowledgeBase: async (query: string) => {
    const res = await fetch(`${API_BASE}/rag/search?query=${encodeURIComponent(query)}`);
    return res.json();
  },

  // Agent Lab
  listAgentTools: async () => {
    const res = await fetch(`${API_BASE}/agent/tools`);
    return res.json();
  },
  executeAgentTask: async (data: {
    task: string;
    provider: string;
    model_name?: string;
    enabled_tools?: string[];
    auto_approve_sensitive?: boolean;
  }) => {
    const res = await fetch(`${API_BASE}/agent/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  approveAgentAction: async (data: {
    execution_id: string;
    action: 'approve' | 'reject';
    rejection_reason?: string;
  }) => {
    const res = await fetch(`${API_BASE}/agent/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  listAgentExecutions: async () => {
    const res = await fetch(`${API_BASE}/agent/executions`);
    return res.json();
  },

  // Red Team Testing
  listRedTeamRisks: async () => {
    const res = await fetch(`${API_BASE}/redteam/risks`);
    return res.json();
  },
  listRedTeamTestCases: async () => {
    const res = await fetch(`${API_BASE}/redteam/test-cases`);
    return res.json();
  },
  runSingleTest: async (data: {
    test_case_id: string;
    provider: string;
    model_name?: string;
  }) => {
    const res = await fetch(`${API_BASE}/redteam/run-single`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  runCampaign: async (data: {
    name?: string;
    target_provider: 'claude' | 'gemini' | 'both';
    risk_ids?: string[];
  }) => {
    const res = await fetch(`${API_BASE}/redteam/run-campaign`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  listTestExecutions: async () => {
    const res = await fetch(`${API_BASE}/redteam/executions`);
    return res.json();
  },

  // Blue Team Mitigations
  toggleMitigation: async (mitigation_id: string, is_active: boolean) => {
    const res = await fetch(`${API_BASE}/blueteam/toggle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mitigation_id, is_active }),
    });
    return res.json();
  },
  runRetest: async (vulnerability_id: string, mitigation_id: string) => {
    const res = await fetch(`${API_BASE}/blueteam/retest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ vulnerability_id, mitigation_id }),
    });
    return res.json();
  },
  getBeforeAfterAnalysis: async () => {
    const res = await fetch(`${API_BASE}/blueteam/before-after`);
    return res.json();
  },

  // MCP
  getMCPStatus: async () => {
    const res = await fetch(`${API_BASE}/mcp/status`);
    return res.json();
  },
  runMCPPoC: async (poc_type: string) => {
    const res = await fetch(`${API_BASE}/mcp/poc`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ poc_type }),
    });
    return res.json();
  },

  // Wazuh
  getWazuhStatus: async () => {
    const res = await fetch(`${API_BASE}/wazuh/status`);
    return res.json();
  },
  getWazuhAlerts: async () => {
    const res = await fetch(`${API_BASE}/wazuh/alerts`);
    return res.json();
  },

  // Audit Logs
  getAuditLogs: async () => {
    const res = await fetch(`${API_BASE}/audit/logs`);
    return res.json();
  },

  // Settings
  getSettings: async () => {
    const res = await fetch(`${API_BASE}/settings/`);
    return res.json();
  },
  updateSettings: async (data: {
    anthropic_api_key?: string;
    gemini_api_key?: string;
    wazuh_api_url?: string;
  }) => {
    const res = await fetch(`${API_BASE}/settings/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
};
