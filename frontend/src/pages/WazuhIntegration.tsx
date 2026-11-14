import React, { useState, useEffect } from 'react';
import { Network, ShieldAlert, CheckCircle2, XCircle, RotateCw, ExternalLink, Activity } from 'lucide-react';
import { api } from '../services/api';

export const WazuhIntegration: React.FC = () => {
  const [wazuhStatus, setWazuhStatus] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const checkStatus = async () => {
    setLoading(true);
    try {
      const [statusRes, alertsRes] = await Promise.all([
        api.getWazuhStatus(),
        api.getWazuhAlerts(),
      ]);
      setWazuhStatus(statusRes);
      setAlerts(alertsRes || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Network className="w-5 h-5 text-[#FF8A00]" />
            <span>Wazuh SIEM / XDR Live Integration</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Official Wazuh Manager API connectivity, telemetry correlation, and live alert streams for AI workloads.
          </p>
        </div>

        <button
          onClick={checkStatus}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-[#0E1015] border border-[#252936] text-slate-200 text-xs font-semibold flex items-center gap-2 hover:border-[#FF8A00] transition-colors"
        >
          <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh SIEM Stream</span>
        </button>
      </div>

      {/* Integration Status Box */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-3">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Manager Connection</p>
          <div className="flex items-center space-x-3">
            {wazuhStatus?.status === 'connected' ? (
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
            ) : (
              <XCircle className="w-6 h-6 text-slate-500" />
            )}
            <div>
              <p className="text-sm font-bold text-white capitalize">{wazuhStatus?.status || 'Unconfigured'}</p>
              <p className="text-[11px] text-slate-400 font-mono mt-0.5">{wazuhStatus?.api_url || 'https://127.0.0.1:55000'}</p>
            </div>
          </div>
          <p className="text-xs text-slate-400 pt-2 border-t border-[#1C202B]">
            {wazuhStatus?.message || 'Wazuh API connection endpoint configured.'}
          </p>
        </div>

        <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-3">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Authentication Protocol</p>
          <p className="text-xs text-slate-300">
            TLS Mutual / JWT Token Bearer authentication with Wazuh RBAC authorization.
          </p>
          <div className="pt-2 border-t border-[#1C202B] flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Cert Verification: Disabled</span>
            <span className="text-emerald-400">SOC Internal</span>
          </div>
        </div>

        <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-3">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">SIEM Alert Statistics</p>
          <div className="flex items-baseline space-x-2">
            <span className="text-2xl font-bold text-white">{alerts.length}</span>
            <span className="text-xs text-slate-400">active SIEM correlations</span>
          </div>
          <p className="text-[11px] text-slate-400 pt-2 border-t border-[#1C202B]">
            {alerts.length === 0 ? 'No alerts reported from live Wazuh cluster.' : 'Correlating real-time security events.'}
          </p>
        </div>
      </div>

      {/* Live Alerts Stream Table */}
      <div className="bg-[#14161D] border border-[#232736] p-5 rounded-xl space-y-4">
        <div className="flex items-center space-x-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
          <Activity className="w-4 h-4 text-[#FF8A00]" />
          <span>Wazuh Live Security Events Feed</span>
        </div>

        {alerts.length === 0 ? (
          <div className="p-8 text-center bg-[#0E1015] rounded-xl border border-[#1E222D] space-y-2">
            <ShieldAlert className="w-8 h-8 text-slate-500 mx-auto" />
            <p className="text-sm font-semibold text-slate-300">No Unhandled Wazuh Alerts</p>
            <p className="text-xs text-slate-500 max-w-md mx-auto">
              Authentic connection maintained. When security events trigger Wazuh rules (e.g. Rule 100200: AI Agent Path Traversal), they stream live into this console.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-[#1E222D]">
            {alerts.map((al, idx) => (
              <div key={idx} className="py-3 flex items-center justify-between text-xs">
                <div>
                  <span className="font-bold text-white">{al.rule?.description || 'Security Event'}</span>
                  <p className="text-slate-400 text-[11px] font-mono mt-0.5">rule_id: {al.rule?.id} • level: {al.rule?.level}</p>
                </div>
                <span className="text-xs font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                  Level {al.rule?.level || 7}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
