import React from 'react';
import { FileText, Download, FileSpreadsheet, Code2, Shield, Calendar, CheckCircle2 } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const handleDownloadPDF = () => {
    window.open('/api/reports/download/pdf', '_blank');
  };

  const handleDownloadCSV = () => {
    window.open('/api/reports/download/csv', '_blank');
  };

  const handleDownloadJSON = () => {
    window.open('/api/reports/download/json', '_blank');
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-[#FF8A00]" />
            <span>Compliance &amp; Security Test Reports</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Export comprehensive security assessment audits, model resilience benchmarks, and forensic evidence.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <Calendar className="w-4 h-4 text-[#FF8A00]" />
          <span>Automated Daily SOC Baseline</span>
        </div>
      </div>

      {/* Export Options Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* PDF Option */}
        <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl space-y-4 hover:border-[#FF8A00]/50 transition-colors shadow-lg">
          <div className="w-12 h-12 rounded-xl bg-[#FF8A00]/10 border border-[#FF8A00]/30 flex items-center justify-center">
            <FileText className="w-6 h-6 text-[#FF8A00]" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Executive PDF Report</h3>
            <p className="text-xs text-slate-400 mt-1">
              Publication-grade audit document including KPI benchmarks, mitigation verification tables, and CISO compliance summaries.
            </p>
          </div>
          <button
            onClick={handleDownloadPDF}
            className="w-full py-2.5 rounded-lg bg-[#FF8A00] hover:bg-[#FFA333] text-black font-bold text-xs flex items-center justify-center gap-2 transition-colors shadow-[0_0_12px_rgba(255,138,0,0.3)]"
          >
            <Download className="w-4 h-4" />
            <span>Download Official PDF</span>
          </button>
        </div>

        {/* CSV Option */}
        <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl space-y-4 hover:border-emerald-500/50 transition-colors shadow-lg">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
            <FileSpreadsheet className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Test Execution CSV</h3>
            <p className="text-xs text-slate-400 mt-1">
              Raw tabular dataset containing all executed test cases, model IDs, latency figures, pass/fail status, and timestamps.
            </p>
          </div>
          <button
            onClick={handleDownloadCSV}
            className="w-full py-2.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-xs flex items-center justify-center gap-2 transition-colors shadow-[0_0_12px_rgba(16,185,129,0.3)]"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV Dataset</span>
          </button>
        </div>

        {/* JSON Option */}
        <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl space-y-4 hover:border-blue-500/50 transition-colors shadow-lg">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center">
            <Code2 className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Forensic JSON Dump</h3>
            <p className="text-xs text-slate-400 mt-1">
              Full machine-readable security snapshot with raw LLM responses, evidence signatures, and mitigation before/after scores.
            </p>
          </div>
          <button
            onClick={handleDownloadJSON}
            className="w-full py-2.5 rounded-lg bg-blue-500 hover:bg-blue-400 text-black font-bold text-xs flex items-center justify-center gap-2 transition-colors shadow-[0_0_12px_rgba(59,130,246,0.3)]"
          >
            <Download className="w-4 h-4" />
            <span>Download JSON Snapshot</span>
          </button>
        </div>
      </div>
    </div>
  );
};
