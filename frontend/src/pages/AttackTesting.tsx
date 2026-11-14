import React, { useState, useEffect } from 'react';
import {
  Crosshair,
  Play,
  RotateCw,
  XCircle,
  AlertTriangle,
  ShieldCheck,
  CheckCircle2,
  Clock,
  ChevronDown,
  ChevronRight,
  Filter,
  Eye
} from 'lucide-react';
import { api } from '../services/api';

export const AttackTesting: React.FC = () => {
  const [testCases, setTestCases] = useState<any[]>([]);
  const [executions, setExecutions] = useState<any[]>([]);
  const [selectedTestCase, setSelectedTestCase] = useState<string>('TC-LLM01-01');
  const [targetProvider, setTargetProvider] = useState<'claude' | 'gemini' | 'both'>('both');
  const [runningCampaign, setRunningCampaign] = useState<boolean>(false);
  const [campaignProgress, setCampaignProgress] = useState<number>(0);
  const [activeTab, setActiveTab] = useState<'all' | 'vulnerable' | 'safe'>('all');
  const [inspectModal, setInspectModal] = useState<any>(null);

  const loadData = async () => {
    try {
      const [tc, execs] = await Promise.all([
        api.listRedTeamTestCases(),
        api.listTestExecutions(),
      ]);
      setTestCases(tc);
      setExecutions(execs);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunSingle = async (testCaseId: string, provider: string) => {
    try {
      await api.runSingleTest({
        test_case_id: testCaseId,
        provider,
      });
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleRunCampaign = async () => {
    setRunningCampaign(true);
    setCampaignProgress(10);
    try {
      await api.runCampaign({
        name: 'OWASP 2026 Red Team Comprehensive Campaign',
        target_provider: targetProvider,
      });
      setCampaignProgress(100);
      loadData();
    } catch (err: any) {
      alert(`Campaign run error: ${err.message}`);
    } finally {
      setRunningCampaign(false);
    }
  };

  const filteredExecutions = executions.filter((e) => {
    if (activeTab === 'vulnerable') return e.result === 'VULNERABLE';
    if (activeTab === 'safe') return e.result === 'SAFE' || e.result === 'BLOCKED';
    return true;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Crosshair className="w-5 h-5 text-[#FF8A00]" />
            <span>Automated AI Red Team Campaign Runner</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Execute 60 multi-model adversarial test cases covering OWASP LLM Top 10 &amp; Agentic Security Initiative (ASI).
          </p>
        </div>

        {/* Campaign Controls */}
        <div className="flex items-center space-x-3">
          <div className="flex bg-[#0E1015] p-1 rounded-lg border border-[#252936] text-xs">
            <button
              onClick={() => setTargetProvider('claude')}
              className={`px-3 py-1.5 rounded font-semibold ${
                targetProvider === 'claude' ? 'bg-[#FF8A00] text-black' : 'text-slate-400 hover:text-white'
              }`}
            >
              Claude Only (30)
            </button>
            <button
              onClick={() => setTargetProvider('gemini')}
              className={`px-3 py-1.5 rounded font-semibold ${
                targetProvider === 'gemini' ? 'bg-[#3B82F6] text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Gemini Only (30)
            </button>
            <button
              onClick={() => setTargetProvider('both')}
              className={`px-3 py-1.5 rounded font-semibold ${
                targetProvider === 'both' ? 'bg-purple-600 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Both Models (60)
            </button>
          </div>

          <button
            onClick={handleRunCampaign}
            disabled={runningCampaign}
            className="px-5 py-2 rounded-lg bg-[#FF8A00] hover:bg-[#FFA333] text-black font-bold text-xs flex items-center gap-2 shadow-[0_0_15px_rgba(255,138,0,0.4)] transition-all disabled:opacity-50"
          >
            {runningCampaign ? <RotateCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4 fill-black" />}
            <span>Run Complete Campaign</span>
          </button>
        </div>
      </div>

      {/* Campaign Progress Bar */}
      {runningCampaign && (
        <div className="bg-[#14161D] border border-[#232736] p-4 rounded-xl space-y-2">
          <div className="flex justify-between text-xs text-slate-300">
            <span>Executing Adversarial Probes... Target: {targetProvider.toUpperCase()}</span>
            <span>Running</span>
          </div>
          <div className="w-full h-2 bg-[#0E1015] rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-[#FF8A00] to-purple-500 animate-pulse w-full rounded-full" />
          </div>
        </div>
      )}

      {/* Main Grid: Test Cases Catalog (Left) & Live Execution Audit Logs (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Test Cases Directory */}
        <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-3 h-[600px] flex flex-col">
          <p className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Adversarial Test Cases ({testCases.length})
          </p>

          <div className="flex-1 overflow-y-auto space-y-2 pr-1">
            {testCases.map((tc) => (
              <div
                key={tc.id}
                className="p-3 rounded-lg bg-[#0E1015] border border-[#1E222D] hover:border-[#FF8A00]/40 transition-colors space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-white">{tc.title}</span>
                  <span className={`text-[10px] font-black px-1.5 py-0.5 rounded ${
                    tc.severity === 'CRITICAL' ? 'bg-red-500 text-black' : 'bg-orange-500 text-black'
                  }`}>
                    {tc.risk_id}
                  </span>
                </div>
                <p className="text-slate-400 text-[11px] line-clamp-2">{tc.attack_prompt}</p>

                <div className="flex items-center justify-between pt-1 border-t border-[#1C202B]">
                  <span className="text-[10px] text-slate-500">{tc.category}</span>
                  <div className="flex space-x-1.5">
                    <button
                      onClick={() => handleRunSingle(tc.id, 'claude')}
                      className="px-2 py-0.5 rounded bg-[#1C202B] hover:bg-[#FF8A00] hover:text-black text-[#FF8A00] text-[10px] font-bold transition-colors"
                    >
                      Claude
                    </button>
                    <button
                      onClick={() => handleRunSingle(tc.id, 'gemini')}
                      className="px-2 py-0.5 rounded bg-[#1C202B] hover:bg-blue-500 hover:text-white text-blue-400 text-[10px] font-bold transition-colors"
                    >
                      Gemini
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Executions Stream Table */}
        <div className="lg:col-span-2 bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-4 h-[600px] flex flex-col">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-xs font-bold text-slate-300">
              <Clock className="w-4 h-4 text-slate-400" />
              <span>Live Test Execution Evidence ({executions.length} runs)</span>
            </div>

            {/* Filter buttons */}
            <div className="flex bg-[#0E1015] p-1 rounded-lg border border-[#202430] text-xs">
              <button
                onClick={() => setActiveTab('all')}
                className={`px-2.5 py-1 rounded font-semibold ${
                  activeTab === 'all' ? 'bg-[#FF8A00] text-black' : 'text-slate-400 hover:text-white'
                }`}
              >
                All
              </button>
              <button
                onClick={() => setActiveTab('vulnerable')}
                className={`px-2.5 py-1 rounded font-semibold ${
                  activeTab === 'vulnerable' ? 'bg-red-500 text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                Vulnerable
              </button>
              <button
                onClick={() => setActiveTab('safe')}
                className={`px-2.5 py-1 rounded font-semibold ${
                  activeTab === 'safe' ? 'bg-emerald-500 text-black' : 'text-slate-400 hover:text-white'
                }`}
              >
                Safe / Blocked
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto space-y-2.5 pr-1">
            {filteredExecutions.map((e) => (
              <div
                key={e.id}
                className="p-3.5 rounded-lg bg-[#0E1015] border border-[#1E222D] flex items-center justify-between text-xs hover:border-slate-700 transition-colors"
              >
                <div className="space-y-1 max-w-lg">
                  <div className="flex items-center space-x-2">
                    <span className={`text-[10px] font-black px-1.5 py-0.5 rounded ${
                      e.result === 'VULNERABLE' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                      'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    }`}>
                      {e.result}
                    </span>
                    <span className="font-bold text-white uppercase">{e.provider}</span>
                    <span className="text-slate-500">• {e.test_case_id}</span>
                    <span className="text-slate-500">• {e.latency_ms}ms</span>
                  </div>
                  <p className="text-slate-300 text-[11px] line-clamp-1">{e.observed_behavior}</p>
                </div>

                <button
                  onClick={() => setInspectModal(e)}
                  className="px-3 py-1.5 rounded-lg bg-[#14161D] border border-[#232736] text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition-colors"
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>Inspect Evidence</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* EVIDENCE INSPECTION MODAL */}
      {inspectModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#14161D] border border-[#232736] rounded-2xl p-6 max-w-2xl w-full space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-[#202430] pb-3">
              <div className="flex items-center space-x-2">
                <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                  inspectModal.result === 'VULNERABLE' ? 'bg-red-500 text-black' : 'bg-emerald-500 text-black'
                }`}>
                  {inspectModal.result}
                </span>
                <span className="font-bold text-white text-sm">Forensic Evidence – {inspectModal.test_case_id}</span>
              </div>
              <button onClick={() => setInspectModal(null)} className="text-slate-400 hover:text-white text-sm">✕</button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <p className="text-[11px] font-bold text-slate-400 uppercase">Adversarial Prompt Payload</p>
                <div className="p-3 bg-[#0E1015] rounded-lg border border-[#202430] font-mono text-slate-200 mt-1 whitespace-pre-wrap">
                  {inspectModal.prompt_payload}
                </div>
              </div>

              <div>
                <p className="text-[11px] font-bold text-slate-400 uppercase">Observed Model Response</p>
                <div className="p-3 bg-[#0E1015] rounded-lg border border-[#202430] font-mono text-slate-200 mt-1 max-h-48 overflow-y-auto whitespace-pre-wrap">
                  {inspectModal.raw_response}
                </div>
              </div>

              <div>
                <p className="text-[11px] font-bold text-slate-400 uppercase">Forensic Analysis</p>
                <p className="text-slate-300 mt-1">{inspectModal.observed_behavior}</p>
              </div>
            </div>

            <div className="flex justify-end pt-3">
              <button
                onClick={() => setInspectModal(null)}
                className="px-4 py-2 rounded-lg bg-[#0E1015] border border-[#252936] text-white text-xs font-bold"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
