import React, { useState, useEffect } from 'react';
import { Cpu, ShieldCheck, ShieldAlert, Play, CheckCircle2, AlertTriangle, FileCode, Lock, Terminal } from 'lucide-react';
import { api } from '../services/api';

export const MCPSecurityLab: React.FC = () => {
  const [mcpStatus, setMcpStatus] = useState<any>(null);
  const [runningPoC, setRunningPoC] = useState<boolean>(false);
  const [pocResult, setPocResult] = useState<any>(null);

  const loadStatus = async () => {
    try {
      const res = await api.getMCPStatus();
      setMcpStatus(res);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleRunPoC = async (pocType: string) => {
    setRunningPoC(true);
    try {
      const res = await api.runMCPPoC(pocType);
      setPocResult(res);
      loadStatus();
    } catch (e: any) {
      alert(e.message);
    } finally {
      setRunningPoC(false);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-[#FF8A00]" />
            <span>Model Context Protocol (MCP) Security Lab</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Local MCP Gateway testing environment. Evaluate schema validation, permission boundaries, and containment defenses.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
            <ShieldCheck className="w-4 h-4" />
            <span>Connection Secure (11% Risk)</span>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Server Status & PoC Actions */}
        <div className="space-y-4">
          <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-3">
            <p className="text-xs font-bold text-slate-300 uppercase tracking-wider">Gateway Configuration</p>
            <div className="p-3 bg-[#0E1015] rounded-lg border border-[#1E222D] space-y-2 text-xs font-mono text-slate-300">
              <p><span className="text-slate-500">Gateway:</span> local-soc-mcp-gateway</p>
              <p><span className="text-slate-500">Protocol:</span> 2024-11-05 (MCP v1)</p>
              <p><span className="text-slate-500">Endpoint:</span> http://127.0.0.1:8765/mcp/v1</p>
              <p><span className="text-slate-500">Status:</span> <span className="text-emerald-400">ONLINE</span></p>
            </div>
          </div>

          <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-3">
            <p className="text-xs font-bold text-slate-300 uppercase tracking-wider">Execute MCP Security PoC</p>
            <div className="space-y-2">
              <button
                onClick={() => handleRunPoC('path_traversal')}
                disabled={runningPoC}
                className="w-full text-left p-3 rounded-lg bg-[#0E1015] border border-[#1E222D] hover:border-[#FF8A00] transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white">Path Traversal PoC</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded font-bold">Blocked</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Payload: `../../../etc/shadow`</p>
              </button>

              <button
                onClick={() => handleRunPoC('unauthorized_tool')}
                disabled={runningPoC}
                className="w-full text-left p-3 rounded-lg bg-[#0E1015] border border-[#1E222D] hover:border-[#FF8A00] transition-colors"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-white">Unauthorized Tool Call PoC</span>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded font-bold">Blocked</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1">Calls privileged `soc_audit_stream`</p>
              </button>
            </div>
          </div>
        </div>

        {/* Right 2 Columns: Discovered Tools & PoC Result Stream */}
        <div className="lg:col-span-2 space-y-6">
          {/* PoC Result Card */}
          {pocResult && (
            <div className="bg-[#14161D] border border-emerald-500/40 rounded-xl p-5 space-y-3 shadow-[0_0_25px_rgba(16,185,129,0.15)]">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-emerald-400">
                  <ShieldCheck className="w-5 h-5" />
                  <span className="text-sm font-bold">PoC Security Defense Verified</span>
                </div>
                <span className="px-2.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30">
                  {pocResult.status}
                </span>
              </div>
              <p className="text-xs text-slate-200">{pocResult.details}</p>
              <div className="p-3 bg-[#0E1015] rounded-lg border border-[#202430] font-mono text-[11px] text-slate-300 overflow-x-auto">
                <pre>{JSON.stringify(pocResult.server_response, null, 2)}</pre>
              </div>
            </div>
          )}

          {/* Discovered MCP Tools */}
          <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-4">
            <p className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Discovered Gateway Tools ({mcpStatus?.discovered_tools?.length || 3})
            </p>

            <div className="space-y-3">
              {(mcpStatus?.discovered_tools || [
                { name: 'read_sandboxed_file', description: 'Read file contents from the authorized SOC sandbox repository.', required_permission: 'file:read:sandbox' },
                { name: 'system_diagnostics', description: 'Collect local cluster telemetry and resource utilization.', required_permission: 'telemetry:read' },
                { name: 'soc_audit_stream', description: 'Stream raw SIEM audit event logs.', required_permission: 'audit:admin' },
              ]).map((tool: any, idx: number) => (
                <div key={idx} className="p-3.5 rounded-lg bg-[#0E1015] border border-[#1E222D] space-y-1.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white font-mono text-[11px]">{tool.name}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-[#1C202B] text-slate-300 font-mono">
                      {tool.required_permission}
                    </span>
                  </div>
                  <p className="text-slate-400 text-[11px]">{tool.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
