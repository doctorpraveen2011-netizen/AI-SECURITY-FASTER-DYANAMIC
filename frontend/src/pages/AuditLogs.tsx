import React, { useState, useEffect } from 'react';
import { History, Shield, Clock, Search, Terminal } from 'lucide-react';
import { api } from '../services/api';

export const AuditLogs: React.FC = () => {
  const [logs, setLogs] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>('');

  const loadLogs = async () => {
    try {
      const res = await api.getAuditLogs();
      setLogs(res || []);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadLogs();
  }, []);

  const filteredLogs = logs.filter(
    (l) =>
      l.action.toLowerCase().includes(filter.toLowerCase()) ||
      l.actor.toLowerCase().includes(filter.toLowerCase()) ||
      l.resource_type.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <History className="w-5 h-5 text-[#FF8A00]" />
            <span>SOC Security Audit Trail</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Immutable forensic audit record logging all test campaigns, agent executions, tool dispatches, and mitigation retests.
          </p>
        </div>

        {/* Filter */}
        <div className="relative w-64">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-500" />
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Filter audit events..."
            className="w-full bg-[#0E1015] border border-[#252936] text-xs text-white placeholder-slate-500 rounded-lg pl-9 pr-3 py-1.5 focus:outline-none focus:border-[#FF8A00]"
          />
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-[#14161D] border border-[#232736] rounded-xl overflow-hidden shadow-lg">
        <div className="p-4 border-b border-[#202430] flex items-center justify-between text-xs font-bold text-slate-400">
          <span>Action &amp; Target</span>
          <span>Actor / IP</span>
          <span>Timestamp</span>
        </div>

        <div className="divide-y divide-[#1A1D27]">
          {filteredLogs.length === 0 ? (
            <div className="p-8 text-center text-slate-500 text-xs">
              No audit logs matching current filter.
            </div>
          ) : (
            filteredLogs.map((log) => (
              <div key={log.id} className="p-4 flex items-center justify-between text-xs hover:bg-[#181B24] transition-colors">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-emerald-400 font-bold">{log.action}</span>
                    <span className="px-1.5 py-0.5 rounded bg-[#0E1015] text-slate-400 text-[10px] font-mono border border-[#252936]">
                      {log.resource_type}
                    </span>
                  </div>
                  {log.details && (
                    <p className="text-[11px] text-slate-400 font-mono">
                      {JSON.stringify(log.details)}
                    </p>
                  )}
                </div>

                <div className="text-right space-y-0.5">
                  <p className="text-slate-300 font-medium">{log.actor}</p>
                  <p className="text-[10px] text-slate-500 font-mono">{log.ip_address}</p>
                </div>

                <div className="text-right text-[11px] text-slate-400 font-mono">
                  {new Date(log.timestamp).toLocaleString()}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
