export interface DashboardMetrics {
  total_tests: number;
  total_tests_trend: string;
  vulnerabilities: number;
  vulnerabilities_trend: string;
  mitigated_risks: number;
  mitigated_trend: string;
  avg_scan_time: string;
  sparklines: {
    total_tests: number[];
    vulnerabilities: number[];
    mitigated: number[];
    scan_time: number[];
  };
}

export interface ModelToolItem {
  id: string;
  name: string;
  version?: string;
  active: boolean;
}

export interface DashboardOverview {
  metrics: DashboardMetrics;
  models_and_tools: {
    models: ModelToolItem[];
    agent_tools: ModelToolItem[];
  };
  mcp_connection: {
    connection_secure: boolean;
    status_label: string;
    risk_score: number;
    poc_result: string;
    poc_badge: string;
  };
  reports_trend: Array<{
    day: string;
    vulnerabilities: number;
    mitigated: number;
  }>;
  last_scan: string;
}

export interface AttackTestCaseSummary {
  risk_id: string;
  name: string;
  test_count: string;
  claude_status: string;
  gemini_status: string;
  claude_pct: number;
  gemini_pct: number;
}

export interface MitigationResultItem {
  id: string;
  name: string;
  risk_id: string;
  before_label: string;
  before_risk_pct: number;
  after_label: string;
  after_risk_pct: number;
  status: string;
  is_active: boolean;
}

export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  tokens_used?: number;
  latency_ms?: number;
  rag_sources?: Array<{
    document_name: string;
    similarity_score: number;
    content: string;
  }>;
  guardrail_flagged?: boolean;
}

export interface AgentStep {
  step_number: number;
  thought: string;
  tool?: string;
  tool_input?: any;
  tool_output?: any;
  is_sensitive?: boolean;
  approval_status?: string;
}

export interface AgentExecution {
  id: string;
  task_input: string;
  provider: string;
  model_name: string;
  status: 'running' | 'completed' | 'waiting_approval' | 'blocked' | 'failed';
  steps: AgentStep[];
  security_alerts: Array<{
    severity: string;
    code: string;
    message: string;
  }>;
  pending_tool_call?: any;
  result?: string;
  created_at: string;
}
