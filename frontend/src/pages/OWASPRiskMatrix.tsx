import React, { useState, useEffect } from 'react';
import { Grid, Shield, ShieldAlert, AlertTriangle, ChevronRight, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export const OWASPRiskMatrix: React.FC = () => {
  const [risks, setRisks] = useState<any[]>([]);
  const [testCases, setTestCases] = useState<any[]>([]);
  const [selectedRisk, setSelectedRisk] = useState<string>('LLM01');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [r, tc] = await Promise.all([
          api.listRedTeamRisks(),
          api.listRedTeamTestCases(),
        ]);
        setRisks(r);
        setTestCases(tc);
      } catch (e) {
        console.error(e);
      }
    };
    fetchData();
  }, []);

  const currentRiskData = risks.find((r) => r.id === selectedRisk) || risks[0];
  const relatedTestCases = testCases.filter((tc) => tc.risk_id === selectedRisk);

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Grid className="w-5 h-5 text-[#FF8A00]" />
            <span>OWASP AI Security Risk Matrix (2026 Taxonomy)</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Authoritative risk taxonomy aligning OWASP Top 10 for LLM Applications and OWASP Agentic Security Initiative (ASI).
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="px-3 py-1 rounded bg-[#0E1015] border border-[#252936] text-[#FF8A00] font-bold">
            5 LLM Risks
          </span>
          <span className="px-3 py-1 rounded bg-[#0E1015] border border-[#252936] text-purple-400 font-bold">
            5 Agentic Risks
          </span>
        </div>
      </div>

      {/* Main Layout: Risk List & Detail Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risks Navigation List */}
        <div className="bg-[#14161D] border border-[#232736] p-4 rounded-xl space-y-2 h-[600px] overflow-y-auto">
          <p className="text-xs font-bold text-slate-400 uppercase px-2 mb-2">Select Risk Category</p>
          {risks.map((r) => {
            const isSelected = r.id === selectedRisk;
            return (
              <button
                key={r.id}
                onClick={() => setSelectedRisk(r.id)}
                className={`w-full text-left p-3 rounded-lg border transition-all flex items-center justify-between ${
                  isSelected
                    ? 'bg-[#1E2330] border-[#FF8A00] text-white shadow-[0_0_12px_rgba(255,138,0,0.25)]'
                    : 'bg-[#0E1015] border-[#1E222D] text-slate-300 hover:border-slate-700'
                }`}
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className={`text-[10px] font-black px-1.5 py-0.5 rounded text-white ${
                      r.framework.includes('ASI') ? 'bg-purple-600' : 'bg-[#FF8A00] text-black'
                    }`}>
                      {r.id}
                    </span>
                    <span className="font-bold text-xs">{r.name}</span>
                  </div>
                  <p className="text-[10px] text-slate-500 mt-1">{r.framework}</p>
                </div>
                <ChevronRight className={`w-4 h-4 ${isSelected ? 'text-[#FF8A00]' : 'text-slate-600'}`} />
              </button>
            );
          })}
        </div>

        {/* Selected Risk Details */}
        <div className="lg:col-span-2 bg-[#14161D] border border-[#232736] p-6 rounded-xl space-y-5 h-[600px] overflow-y-auto">
          {currentRiskData ? (
            <>
              <div className="flex items-center justify-between pb-4 border-b border-[#202430]">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-lg font-black text-[#FF8A00]">{currentRiskData.id}:</span>
                    <span className="text-lg font-bold text-white">{currentRiskData.name}</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">{currentRiskData.framework}</p>
                </div>

                <span className={`text-xs font-black px-2.5 py-1 rounded text-white ${
                  currentRiskData.severity === 'CRITICAL' ? 'bg-red-500' : 'bg-orange-500'
                }`}>
                  {currentRiskData.severity} SEVERITY
                </span>
              </div>

              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Taxonomy Description</p>
                <p className="text-sm text-slate-200 mt-1.5 leading-relaxed bg-[#0E1015] p-4 rounded-xl border border-[#202430]">
                  {currentRiskData.description}
                </p>
              </div>

              {/* Related Test Cases */}
              <div className="space-y-3">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  Associated Red Team Test Cases ({relatedTestCases.length})
                </p>

                <div className="space-y-2.5">
                  {relatedTestCases.map((tc) => (
                    <div key={tc.id} className="p-3.5 rounded-xl bg-[#0E1015] border border-[#1E222D] space-y-2 text-xs">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-white text-xs">{tc.title}</span>
                        <span className="text-[10px] text-slate-400 font-mono">{tc.id}</span>
                      </div>
                      <p className="text-slate-400 text-[11px] font-mono bg-[#14161D] p-2 rounded border border-[#232736]">
                        {tc.attack_prompt}
                      </p>
                      <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1">
                        <span>Expected safe behavior: {tc.expected_safe_behavior}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <p className="text-slate-400 text-xs">Loading risk details...</p>
          )}
        </div>
      </div>
    </div>
  );
};
