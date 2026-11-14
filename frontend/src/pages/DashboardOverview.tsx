import React, { useEffect, useState } from 'react';
import {
  Shield,
  ShieldAlert,
  ShieldCheck,
  Clock,
  ChevronRight,
  Download,
  AlertTriangle,
  FileCode,
  Mail,
  Globe,
  Cpu,
  Check,
  Lock,
  Calendar,
  Bot
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';
import { Sparkline } from '../components/Sparkline';
import { BrainGraphic } from '../components/BrainGraphic';
import { api } from '../services/api';

interface DashboardOverviewProps {
  onNavigate: (tab: string) => void;
  currentProvider: 'claude' | 'gemini';
  onProviderChange: (provider: 'claude' | 'gemini') => void;
}

export const DashboardOverview: React.FC<DashboardOverviewProps> = ({
  onNavigate,
  currentProvider,
  onProviderChange,
}) => {
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<any>({
    total_tests: 48,
    total_tests_trend: '+12%',
    vulnerabilities: 27,
    vulnerabilities_trend: '+8%',
    mitigated_risks: 24,
    mitigated_trend: '+15%',
    avg_scan_time: '2m 14s',
    sparklines: {
      total_tests: [30, 34, 38, 41, 45, 48],
      vulnerabilities: [18, 20, 23, 24, 26, 27],
      mitigated: [12, 14, 17, 19, 22, 24],
      scan_time: [145, 140, 138, 135, 134, 134],
    },
  });

  const [activeCoverageTab, setActiveCoverageTab] = useState<'llm' | 'agentic'>('llm');
  const [testCases, setTestCases] = useState<any[]>([]);
  const [mitigations, setMitigations] = useState<any[]>([]);
  const [mcpData, setMcpData] = useState<any>({
    risk_score: 11.0,
    poc_result: 'Attempted path traversal (../../../etc/shadow) blocked.',
  });

  const chartData = [
    { day: 'Mon', vulnerabilities: 12, mitigated: 5 },
    { day: 'Tue', vulnerabilities: 25, mitigated: 14 },
    { day: 'Wed', vulnerabilities: 30, mitigated: 20 },
    { day: 'Thu', vulnerabilities: 28, mitigated: 24 },
    { day: 'Fri', vulnerabilities: 45, mitigated: 35 },
    { day: 'Sat', vulnerabilities: 42, mitigated: 38 },
    { day: 'Sun', vulnerabilities: 48, mitigated: 43 },
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, testsRes, mitRes] = await Promise.all([
          api.getDashboardOverview(),
          api.getRecentTests(),
          api.getMitigations(),
        ]);
        if (overviewRes && overviewRes.metrics) {
          setMetrics(overviewRes.metrics);
          if (overviewRes.mcp_connection) {
            setMcpData(overviewRes.mcp_connection);
          }
        }
        if (testsRes) setTestCases(testsRes);
        if (mitRes && mitRes.items) setMitigations(mitRes.items);
      } catch (err) {
        console.error('Error fetching dashboard overview:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleDownloadReport = () => {
    window.open('/api/reports/download/pdf', '_blank');
  };

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      {/* 1. WELCOME HERO BANNER */}
      <div className="relative rounded-2xl bg-gradient-to-r from-[#14161D] via-[#161822] to-[#12141A] border border-[#232736] p-7 overflow-hidden shadow-2xl">
        <div className="flex items-center justify-between relative z-10">
          <div className="flex items-center space-x-5">
            {/* Glowing Orange Shield with Lock */}
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#FF8A00] to-[#B35F00] p-0.5 shadow-[0_0_30px_rgba(255,138,0,0.45)] flex items-center justify-center">
              <div className="w-full h-full bg-[#14161D] rounded-2xl flex items-center justify-center">
                <Lock className="w-8 h-8 text-[#FF8A00] drop-shadow-[0_0_8px_rgba(255,138,0,0.8)]" />
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                Welcome to <span className="text-white">AI Security Faster</span>
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                Automated Red-Teaming &amp; Blue-Teaming for LLMs and AI Agents
              </p>
            </div>
          </div>

          {/* Wireframe Glowing Brain Graphic & Tagline */}
          <div className="flex items-center space-x-6">
            <BrainGraphic className="w-52 h-28 hidden md:block" />
            <div className="hidden lg:block text-right">
              <p className="text-xs font-semibold text-slate-400 tracking-wider">
                Test <span className="text-[#FF8A00]">•</span> Detect <span className="text-[#FF8A00]">•</span> Mitigate <span className="text-[#FF8A00]">•</span> Stay Secure
              </p>
            </div>
          </div>
        </div>

        {/* Ambient subtle glow overlay */}
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-[#FF8A00]/5 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* 2. TOP METRIC CARDS (4 KPIs with Sparklines) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* KPI 1: Total Tests Run */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-5 flex items-center justify-between hover:border-[#FF8A00]/40 transition-colors shadow-lg">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-[#FF8A00]/10 border border-[#FF8A00]/30 flex items-center justify-center">
              <Shield className="w-6 h-6 text-[#FF8A00]" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Total Tests Run</p>
              <div className="flex items-baseline space-x-2 mt-0.5">
                <span className="text-2xl font-bold text-white tracking-tight">{metrics.total_tests}</span>
                <span className="text-xs font-semibold text-[#FF8A00] flex items-center">
                  ↑{metrics.total_tests_trend}
                </span>
              </div>
            </div>
          </div>
          <Sparkline data={metrics.sparklines?.total_tests || [30, 35, 40, 48]} color="#FF8A00" />
        </div>

        {/* KPI 2: Vulnerabilities Found */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-5 flex items-center justify-between hover:border-red-500/40 transition-colors shadow-lg">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-red-500/10 border border-red-500/30 flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-red-500" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Vulnerabilities Found</p>
              <div className="flex items-baseline space-x-2 mt-0.5">
                <span className="text-2xl font-bold text-white tracking-tight">{metrics.vulnerabilities}</span>
                <span className="text-xs font-semibold text-red-400 flex items-center">
                  ↑{metrics.vulnerabilities_trend}
                </span>
              </div>
            </div>
          </div>
          <Sparkline data={metrics.sparklines?.vulnerabilities || [18, 22, 25, 27]} color="#EF4444" />
        </div>

        {/* KPI 3: Mitigated Risks */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-5 flex items-center justify-between hover:border-emerald-500/40 transition-colors shadow-lg">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6 text-emerald-500" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Mitigated Risks</p>
              <div className="flex items-baseline space-x-2 mt-0.5">
                <span className="text-2xl font-bold text-white tracking-tight">{metrics.mitigated_risks}</span>
                <span className="text-xs font-semibold text-emerald-400 flex items-center">
                  ↑{metrics.mitigated_trend}
                </span>
              </div>
            </div>
          </div>
          <Sparkline data={metrics.sparklines?.mitigated || [12, 16, 20, 24]} color="#10B981" />
        </div>

        {/* KPI 4: Avg Scan Time */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-5 flex items-center justify-between hover:border-purple-500/40 transition-colors shadow-lg">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center">
              <Clock className="w-6 h-6 text-purple-400" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">Avg Scan Time</p>
              <div className="flex items-baseline space-x-2 mt-0.5">
                <span className="text-2xl font-bold text-white tracking-tight">{metrics.avg_scan_time}</span>
              </div>
            </div>
          </div>
          <Sparkline data={metrics.sparklines?.scan_time || [145, 140, 136, 134]} color="#A855F7" />
        </div>
      </div>

      {/* 3. MIDDLE ROW: Models & Tools (Left) & Risk Coverage OWASP 2026 (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Card: Models & Tools */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-6 shadow-lg">
          <div className="flex items-center space-x-2 text-sm font-bold text-white mb-5">
            <Bot className="w-4 h-4 text-slate-400" />
            <span>Models &amp; Tools</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Models Box */}
            <div className="bg-[#0E1015] border border-[#1E222D] rounded-xl p-4">
              <p className="text-[11px] font-medium text-slate-400 mb-3">Target LLMs</p>
              <div className="flex space-x-3">
                <button
                  onClick={() => onProviderChange('claude')}
                  className={`flex-1 py-2.5 px-3 rounded-lg border text-xs font-semibold flex items-center justify-center space-x-2 transition-all ${
                    currentProvider === 'claude'
                      ? 'border-[#FF8A00] bg-[#1A1D27] text-white shadow-[0_0_12px_rgba(255,138,0,0.25)]'
                      : 'border-[#262A37] text-slate-400 hover:text-white'
                  }`}
                >
                  <svg className="w-4 h-4 text-[#FF8A00]" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2l1.5 5.5L19 9l-5.5 1.5L12 16l-1.5-5.5L5 9l5.5-1.5z" />
                    <circle cx="12" cy="12" r="3" fill="#FF8A00" />
                  </svg>
                  <span>Claude</span>
                </button>

                <button
                  onClick={() => onProviderChange('gemini')}
                  className={`flex-1 py-2.5 px-3 rounded-lg border text-xs font-semibold flex items-center justify-center space-x-2 transition-all ${
                    currentProvider === 'gemini'
                      ? 'border-[#3B82F6] bg-[#1A1D27] text-white shadow-[0_0_12px_rgba(59,130,246,0.25)]'
                      : 'border-[#262A37] text-slate-400 hover:text-white'
                  }`}
                >
                  <span className="w-4 h-4 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-[10px]">
                    G
                  </span>
                  <span>Gemini</span>
                </button>
              </div>
            </div>

            {/* Agent Tools (2-4) Box */}
            <div className="bg-[#0E1015] border border-[#1E222D] rounded-xl p-4">
              <p className="text-[11px] font-medium text-slate-400 mb-3">Agent Tools (2-4)</p>
              <div className="grid grid-cols-2 gap-2">
                <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded-lg bg-[#14161D] border border-[#252936] text-[11px] text-slate-200">
                  <FileCode className="w-3.5 h-3.5 text-blue-400" />
                  <span>File Read</span>
                </div>
                <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded-lg bg-[#14161D] border border-[#252936] text-[11px] text-slate-200">
                  <Mail className="w-3.5 h-3.5 text-emerald-400" />
                  <span>Email</span>
                </div>
                <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded-lg bg-[#14161D] border border-[#252936] text-[11px] text-slate-200">
                  <Globe className="w-3.5 h-3.5 text-purple-400" />
                  <span>HTTP Call</span>
                </div>
                <div className="flex items-center space-x-2 px-2.5 py-1.5 rounded-lg bg-[#14161D] border border-[#252936] text-[11px] text-slate-200">
                  <Cpu className="w-3.5 h-3.5 text-[#FF8A00]" />
                  <span>MCP Tools</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Card: Risk Coverage (OWASP 2026) */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-6 shadow-lg">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center space-x-2 text-sm font-bold text-white">
              <Shield className="w-4 h-4 text-[#FF8A00]" />
              <span>Risk Coverage (OWASP 2026)</span>
            </div>

            {/* Switcher Tab */}
            <div className="flex bg-[#0E1015] p-1 rounded-lg border border-[#202430]">
              <button
                onClick={() => setActiveCoverageTab('llm')}
                className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                  activeCoverageTab === 'llm'
                    ? 'bg-[#FF8A00] text-black'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                LLM Top 10
              </button>
              <button
                onClick={() => setActiveCoverageTab('agentic')}
                className={`px-3 py-1 rounded text-xs font-semibold transition-all ${
                  activeCoverageTab === 'agentic'
                    ? 'bg-[#FF8A00] text-black'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Agentic Top 10
              </button>
            </div>
          </div>

          {/* Risk Badges */}
          {activeCoverageTab === 'llm' ? (
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">LLM01:</span>
                <span>Prompt Injection</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">LLM02:</span>
                <span>Sensitive Info</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">LLM08:</span>
                <span>Excessive Agency</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">LLM10:</span>
                <span>Vector Misuse</span>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">ASI01:</span>
                <span>Jailbreak Agents</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">ASI02:</span>
                <span>Tool Misuse</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">ASI03:</span>
                <span>Goal Misalignment</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">ASI05:</span>
                <span>Data Leakage</span>
              </div>
              <div className="flex items-center space-x-2 text-xs text-slate-300">
                <span className="w-2 h-2 rounded-full bg-[#FF8A00]" />
                <span className="font-semibold text-slate-200">ASI06:</span>
                <span>Privilege Escalation</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* 4. LOWER MIDDLE ROW: Attack Test Cases (Left) & Mitigation Results (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Card: Attack Test Cases */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-6 shadow-lg">
          <div className="flex items-center space-x-2 text-sm font-bold text-white mb-5">
            <span className="text-[#FF8A00] font-black">✕</span>
            <span>Attack Test Cases</span>
          </div>

          <div className="space-y-4">
            {(testCases.length > 0 ? testCases : [
              { risk_id: 'LLM01', name: 'Prompt Injection', test_count: '3+ Tests', claude_status: '3/3 ✓', gemini_status: '3/3 ✓' },
              { risk_id: 'LLM02', name: 'Sensitive Information', test_count: '3+ Tests', claude_status: '3/3 ✓', gemini_status: '3/3 ✓' },
              { risk_id: 'LLM03', name: 'Supply Chain Attacks', test_count: '3+ Tests', claude_status: '3/3 ✓', gemini_status: '3/3 ✓' },
              { risk_id: 'LLM08', name: 'Excessive Agency', test_count: '3+ Tests', claude_status: '3/3 ✓', gemini_status: '3/3 ✓' },
              { risk_id: 'LLM10', name: 'Vector Misuse', test_count: '3+ Tests', claude_status: '3/3 ✓', gemini_status: '3/3 ✓' },
            ]).map((tc, idx) => (
              <div
                key={idx}
                onClick={() => onNavigate('attack-testing')}
                className="flex items-center justify-between p-2.5 rounded-lg bg-[#0E1015] border border-[#1E222D] hover:border-[#FF8A00]/40 cursor-pointer transition-colors"
              >
                {/* Risk ID Pill */}
                <div className="flex items-center space-x-3 w-48">
                  <span className={`text-[10px] font-black px-2 py-0.5 rounded text-white ${
                    tc.risk_id === 'LLM01' ? 'bg-red-500' :
                    tc.risk_id === 'LLM02' ? 'bg-orange-500' :
                    tc.risk_id === 'LLM03' ? 'bg-purple-600' :
                    tc.risk_id === 'LLM08' ? 'bg-emerald-600' : 'bg-blue-600'
                  }`}>
                    {tc.risk_id}
                  </span>
                  <div>
                    <p className="text-xs font-semibold text-white leading-tight">{tc.name}</p>
                    <p className="text-[10px] text-slate-500">{tc.test_count}</p>
                  </div>
                </div>

                {/* Claude Status */}
                <div className="flex items-center space-x-2">
                  <span className="text-[11px] text-slate-400">Claude</span>
                  <div className="w-16 h-2 bg-[#202430] rounded-full overflow-hidden">
                    <div className="h-full bg-[#FF8A00] w-full rounded-full" />
                  </div>
                  <span className="text-[11px] font-medium text-emerald-400">3/3 ✓</span>
                </div>

                {/* Gemini Status */}
                <div className="flex items-center space-x-2">
                  <span className="text-[11px] text-slate-400">Gemini</span>
                  <div className="w-16 h-2 bg-[#202430] rounded-full overflow-hidden">
                    <div className="h-full bg-[#FF8A00] w-full rounded-full" />
                  </div>
                  <span className="text-[11px] font-medium text-emerald-400">3/3 ✓</span>
                </div>

                <ChevronRight className="w-4 h-4 text-slate-500" />
              </div>
            ))}
          </div>
        </div>

        {/* Card: Mitigation Results */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-6 shadow-lg">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center space-x-2 text-sm font-bold text-white">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>Mitigation Results</span>
            </div>

            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
              <Check className="w-3.5 h-3.5" />
              <span>All Mitigations Applied ✓</span>
            </div>
          </div>

          {/* Table Header */}
          <div className="grid grid-cols-12 text-[11px] font-semibold text-slate-400 pb-2 border-b border-[#1E222D]">
            <span className="col-span-5">Risk Category</span>
            <span className="col-span-3 text-center">Before Mitigation</span>
            <span className="col-span-1 text-center"></span>
            <span className="col-span-3 text-center">After Mitigation</span>
          </div>

          {/* Table Rows */}
          <div className="divide-y divide-[#1A1D27] mt-1">
            {(mitigations.length > 0 ? mitigations : [
              { name: 'Prompt Injection (LLM01)', before_label: 'High Risk (87%)', after_label: 'Low Risk (12%)' },
              { name: 'Sensitive Information (LLM02)', before_label: 'High Risk (82%)', after_label: 'Low Risk (9%)' },
              { name: 'Agent Tool Misuse (ASI05)', before_label: 'Medium (61%)', after_label: 'Low Risk (14%)' },
              { name: 'MCP Connection Risk', before_label: 'High Risk (79%)', after_label: 'Low Risk (11%)' },
            ]).map((m, idx) => (
              <div key={idx} className="grid grid-cols-12 items-center py-3 text-xs">
                <div className="col-span-5 flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-red-400" />
                  <span className="font-medium text-slate-200">{m.name}</span>
                </div>
                <div className="col-span-3 text-center">
                  <span className="px-2 py-0.5 rounded bg-red-500/10 text-red-400 font-semibold border border-red-500/20 text-[11px]">
                    {m.before_label}
                  </span>
                </div>
                <div className="col-span-1 text-center text-slate-500 font-bold">→</div>
                <div className="col-span-3 text-center">
                  <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-semibold border border-emerald-500/20 text-[11px]">
                    {m.after_label}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 5. BOTTOM ROW: MCP Connection Risk (Left) & Test Reports Trend (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Card: MCP Connection Risk */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-6 shadow-lg">
          <div className="flex items-center space-x-2 text-sm font-bold text-white mb-5">
            <Cpu className="w-4 h-4 text-[#FF8A00]" />
            <span>MCP Connection Risk</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
            {/* Left Score Box */}
            <div className="md:col-span-5 bg-[#0E1015] border border-emerald-500/30 rounded-xl p-4 flex flex-col items-center justify-center text-center shadow-[0_0_15px_rgba(16,185,129,0.15)]">
              <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center mb-2">
                <ShieldCheck className="w-6 h-6 text-emerald-400" />
              </div>
              <p className="text-xs font-bold text-white">Connection Secure</p>
              <p className="text-xs font-semibold text-emerald-400 mt-0.5">
                Risk Score: {mcpData.risk_score || 11}%
              </p>
            </div>

            {/* Right PoC Box */}
            <div className="md:col-span-7 bg-[#0E1015] border border-[#1E222D] rounded-xl p-4 flex flex-col justify-between space-y-3">
              <div>
                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">POC Result</p>
                <p className="text-xs font-medium text-slate-300 mt-1">
                  {mcpData.poc_result || 'Attempted path traversal (../../../etc/shadow) blocked.'}
                </p>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-[#1C1F2B]">
                <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" /> Blocked
                </span>

                <button
                  onClick={() => onNavigate('mcp-lab')}
                  className="text-xs font-semibold text-[#FF8A00] hover:text-[#FFA733] flex items-center space-x-1"
                >
                  <span>View Details</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Card: Test Reports Trend Chart */}
        <div className="bg-[#14161D] rounded-xl border border-[#232736] p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2 text-sm font-bold text-white">
              <Calendar className="w-4 h-4 text-[#FF8A00]" />
              <span>Test Reports</span>
            </div>

            <div className="flex items-center space-x-4">
              {/* Legend */}
              <div className="flex items-center space-x-3 text-xs">
                <span className="flex items-center gap-1.5 text-slate-300">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#FF8A00]" /> Vulnerabilities
                </span>
                <span className="flex items-center gap-1.5 text-slate-300">
                  <span className="w-2.5 h-2.5 rounded-full bg-[#10B981]" /> Mitigated
                </span>
              </div>

              {/* Download Report Button */}
              <button
                onClick={handleDownloadReport}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border border-[#FF8A00] text-[#FF8A00] hover:bg-[#FF8A00] hover:text-black transition-colors text-xs font-bold shadow-[0_0_12px_rgba(255,138,0,0.2)]"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Report</span>
              </button>
            </div>
          </div>

          {/* Recharts Dual-Line Chart */}
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E222D" />
                <XAxis dataKey="day" stroke="#64748B" fontSize={11} />
                <YAxis stroke="#64748B" fontSize={11} domain={[0, 50]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#14161D',
                    borderColor: '#252936',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="vulnerabilities"
                  stroke="#FF8A00"
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: '#FF8A00' }}
                />
                <Line
                  type="monotone"
                  dataKey="mitigated"
                  stroke="#10B981"
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: '#10B981' }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Last Scan Footer */}
          <div className="flex items-center justify-end space-x-2 text-[11px] text-slate-500 mt-2">
            <Clock className="w-3 h-3" />
            <span>Last Scan: Nov 12, 2026 • 19:45</span>
          </div>
        </div>
      </div>
    </div>
  );
};
