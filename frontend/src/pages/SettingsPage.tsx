import React, { useState, useEffect } from 'react';
import { Settings, Key, Database, Network, ShieldCheck, CheckCircle2, AlertTriangle, Save, RotateCw } from 'lucide-react';
import { api } from '../services/api';

export const SettingsPage: React.FC = () => {
  const [settingsData, setSettingsData] = useState<any>(null);
  const [anthropicKey, setAnthropicKey] = useState<string>('');
  const [geminiKey, setGeminiKey] = useState<string>('');
  const [wazuhUrl, setWazuhUrl] = useState<string>('');
  const [modelStatus, setModelStatus] = useState<any>(null);
  const [saving, setSaving] = useState<boolean>(false);
  const [saveSuccess, setSaveSuccess] = useState<boolean>(false);

  const loadData = async () => {
    try {
      const [s, statusRes] = await Promise.all([
        api.getSettings(),
        api.getModelStatus(),
      ]);
      setSettingsData(s);
      setModelStatus(statusRes);
      if (s) {
        setWazuhUrl(s.wazuh_api_url || '');
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaveSuccess(false);
    try {
      await api.updateSettings({
        anthropic_api_key: anthropicKey ? anthropicKey.trim() : undefined,
        gemini_api_key: geminiKey ? geminiKey.trim() : undefined,
        wazuh_api_url: wazuhUrl ? wazuhUrl.trim() : undefined,
      });
      setAnthropicKey('');
      setGeminiKey('');
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
      loadData();
    } catch (e: any) {
      alert(`Save error: ${e.message}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      {/* Top Banner */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl shadow-lg flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Settings className="w-5 h-5 text-[#FF8A00]" />
            <span>Platform Settings &amp; API Key Management</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Configure official Anthropic and Google Gen AI API keys, SIEM endpoints, and security thresholds.
          </p>
        </div>

        {saveSuccess && (
          <div className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold animate-fade-in">
            <CheckCircle2 className="w-4 h-4" />
            <span>Keys Updated Successfully</span>
          </div>
        )}
      </div>

      {/* Frontier LLM Keys */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl space-y-6 shadow-lg">
        <div className="flex items-center space-x-2 text-sm font-bold text-white border-b border-[#202430] pb-3">
          <Key className="w-4 h-4 text-[#FF8A00]" />
          <span>Frontier AI Model API Credentials</span>
        </div>

        {/* Anthropic Claude API Key */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-200 flex items-center gap-2">
              <span>Anthropic Claude API Key</span>
              {modelStatus?.claude?.status === 'connected' ? (
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">
                  CONNECTED
                </span>
              ) : (
                <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">
                  {settingsData?.anthropic_configured ? 'KEY SET' : 'UNCONFIGURED'}
                </span>
              )}
            </label>
            {settingsData?.anthropic_masked && (
              <span className="text-xs font-mono text-slate-500">Current: {settingsData.anthropic_masked}</span>
            )}
          </div>
          <input
            type="password"
            value={anthropicKey}
            onChange={(e) => setAnthropicKey(e.target.value)}
            placeholder="sk-ant-api03-..."
            className="w-full bg-[#0E1015] border border-[#252936] text-white text-xs rounded-lg p-3 font-mono focus:outline-none focus:border-[#FF8A00]"
          />
          <p className="text-[11px] text-slate-500">
            Keys are securely loaded into the backend memory and never exposed to client-side code.
          </p>
        </div>

        {/* Google Gemini API Key */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <label className="text-xs font-bold text-slate-200 flex items-center gap-2">
              <span>Google Gemini API Key</span>
              {modelStatus?.gemini?.status === 'connected' ? (
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold">
                  CONNECTED
                </span>
              ) : (
                <span className="text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30 font-bold">
                  {settingsData?.gemini_configured ? 'KEY SET' : 'UNCONFIGURED'}
                </span>
              )}
            </label>
            {settingsData?.gemini_masked && (
              <span className="text-xs font-mono text-slate-500">Current: {settingsData.gemini_masked}</span>
            )}
          </div>
          <input
            type="password"
            value={geminiKey}
            onChange={(e) => setGeminiKey(e.target.value)}
            placeholder="AIzaSy..."
            className="w-full bg-[#0E1015] border border-[#252936] text-white text-xs rounded-lg p-3 font-mono focus:outline-none focus:border-[#3B82F6]"
          />
          <p className="text-[11px] text-slate-500">
            Obtain your API key from Google AI Studio (https://aistudio.google.com).
          </p>
        </div>
      </div>

      {/* SIEM & Infrastructure */}
      <div className="bg-[#14161D] border border-[#232736] p-6 rounded-xl space-y-6 shadow-lg">
        <div className="flex items-center space-x-2 text-sm font-bold text-white border-b border-[#202430] pb-3">
          <Network className="w-4 h-4 text-[#FF8A00]" />
          <span>Wazuh SIEM &amp; Database Configuration</span>
        </div>

        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-200">Wazuh Manager API Endpoint</label>
          <input
            type="text"
            value={wazuhUrl}
            onChange={(e) => setWazuhUrl(e.target.value)}
            placeholder="https://127.0.0.1:55000"
            className="w-full bg-[#0E1015] border border-[#252936] text-white text-xs rounded-lg p-3 font-mono focus:outline-none focus:border-[#FF8A00]"
          />
        </div>

        <div className="space-y-2">
          <label className="text-xs font-bold text-slate-200">Active Database Storage</label>
          <div className="p-3 bg-[#0E1015] rounded-lg border border-[#252936] text-xs font-mono text-slate-400">
            {settingsData?.database_url || 'sqlite:///./ai_security.db'}
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-6 py-2.5 rounded-lg bg-[#FF8A00] hover:bg-[#FFA333] text-black font-bold text-xs flex items-center gap-2 shadow-[0_0_15px_rgba(255,138,0,0.4)] transition-all disabled:opacity-50"
        >
          {saving ? <RotateCw className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
          <span>Save &amp; Reload Credentials</span>
        </button>
      </div>
    </div>
  );
};
