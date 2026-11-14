import React, { useState, useEffect } from 'react';
import { ShieldCheck, ShieldAlert, ToggleLeft, ToggleRight, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

export const BlueTeamMitigations: React.FC = () => {
  const [mitigations, setMitigations] = useState<any[]>([]);

  const loadData = async () => {
    try {
      const res = await api.getMitigations();
      if (res && res.items) setMitigations(res.items);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleToggle = async (id: string, currentState: boolean) => {
    try {
      await api.toggleMitigation(id, !currentState);
      loadData();
    } catch (e: any) {
      alert(e.message);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <span>Blue Team Active Defenses &amp; Mitigations</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time input firewalls, output token sanitizers, tool whitelists, and SSRF filters protecting frontier models.
          </p>
        </div>

        <span className="px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold flex items-center gap-1.5">
          <CheckCircle2 className="w-3.5 h-3.5" /> All Defensive Systems Active
        </span>
      </div>

      {/* Mitigations List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {mitigations.map((m) => (
          <div
            key={m.id}
            className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-4 shadow-lg hover:border-emerald-500/30 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div>
                <span className="text-[10px] font-black px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 uppercase tracking-wider">
                  {m.risk_id}
                </span>
                <h3 className="text-sm font-bold text-white mt-1.5">{m.name}</h3>
              </div>

              <button
                onClick={() => handleToggle(m.id, m.is_active)}
                className="text-slate-400 hover:text-white"
              >
                {m.is_active ? (
                  <ToggleRight className="w-8 h-8 text-emerald-400" />
                ) : (
                  <ToggleLeft className="w-8 h-8 text-slate-600" />
                )}
              </button>
            </div>

            {/* Risk Reduction Badge */}
            <div className="flex items-center space-x-3 p-3 bg-[#0E1015] rounded-xl border border-[#1E222D] text-xs">
              <span className="text-red-400 font-semibold">{m.before_label}</span>
              <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
              <span className="text-emerald-400 font-bold">{m.after_label}</span>
              <span className="ml-auto text-[10px] text-slate-400 font-mono">
                {Math.round(m.before_risk_pct - m.after_risk_pct)}% reduction
              </span>
            </div>

            <div className="flex items-center justify-between text-[11px] pt-1 border-t border-[#1C202B]">
              <span className="text-slate-400 font-mono">status: {m.status}</span>
              <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                m.is_active ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'
              }`}>
                {m.is_active ? 'ENFORCING' : 'DISABLED'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
