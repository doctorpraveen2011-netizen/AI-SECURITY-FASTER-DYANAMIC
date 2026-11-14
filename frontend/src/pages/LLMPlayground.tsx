import React, { useState, useEffect } from 'react';
import {
  Send,
  Sparkles,
  Bot,
  Sliders,
  Database,
  Shield,
  Columns,
  RotateCcw,
  Download,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Cpu
} from 'lucide-react';
import { api } from '../services/api';
import { ChatMessage } from '../types';

export const LLMPlayground: React.FC = () => {
  const [provider, setProvider] = useState<'claude' | 'gemini'>('claude');
  const [modelName, setModelName] = useState<string>('claude-3-5-sonnet-20241022');
  const [systemPrompt, setSystemPrompt] = useState<string>(
    'You are a cybersecurity intelligence assistant specialized in AI security, red teaming, and defensive mitigations.'
  );
  const [useRAG, setUseRAG] = useState<boolean>(true);
  const [applyGuardrails, setApplyGuardrails] = useState<boolean>(true);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Welcome to the Dual-Model AI Security Playground. I am connected to the enterprise SOC RAG knowledge base. Select Claude or Gemini, adjust system guardrails, or trigger side-by-side evaluations.',
      tokens_used: 35,
      latency_ms: 50
    }
  ]);
  const [inputPrompt, setInputPrompt] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [isCompareMode, setIsCompareMode] = useState<boolean>(false);
  const [comparisonResult, setComparisonResult] = useState<any>(null);

  useEffect(() => {
    if (provider === 'claude') {
      setModelName('claude-3-5-sonnet-20241022');
    } else {
      setModelName('gemini-1.5-flash');
    }
  }, [provider]);

  const handleSendMessage = async () => {
    if (!inputPrompt.trim() || loading) return;

    const userMsg: ChatMessage = { role: 'user', content: inputPrompt };
    setMessages((prev) => [...prev, userMsg]);
    const promptToSend = inputPrompt;
    setInputPrompt('');
    setLoading(true);

    try {
      if (isCompareMode) {
        const compareRes = await api.compareModels({
          prompt: promptToSend,
          system_prompt: systemPrompt,
        });
        setComparisonResult(compareRes);
      } else {
        const res = await api.sendChat({
          provider,
          model_name: modelName,
          system_prompt: systemPrompt,
          messages: [...messages, userMsg].map((m) => ({ role: m.role, content: m.content })),
          use_rag: useRAG,
          apply_guardrails: applyGuardrails,
        });

        const assistantMsg: ChatMessage = {
          role: 'assistant',
          content: res.response,
          tokens_used: res.tokens_used,
          latency_ms: res.latency_ms,
          rag_sources: res.rag_sources,
          guardrail_flagged: res.guardrail_flagged,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      }
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Error invoking ${provider}: ${err.message || 'Check API key or server status.'}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Conversation reset. Ready for new security prompts.',
      },
    ]);
    setComparisonResult(null);
  };

  const handleExportChat = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(messages, null, 2));
    const dlAnchorElem = document.createElement('a');
    dlAnchorElem.setAttribute('href', dataStr);
    dlAnchorElem.setAttribute('download', `chat_export_${provider}_${Date.now()}.json`);
    dlAnchorElem.click();
  };

  return (
    <div className="p-8 max-w-7xl mx-auto h-[calc(100vh-4rem)] flex flex-col space-y-4">
      {/* Header Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-[#14161D] border border-[#232736] p-4 rounded-xl shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="flex bg-[#0E1015] p-1 rounded-lg border border-[#252936]">
            <button
              onClick={() => { setProvider('claude'); setIsCompareMode(false); }}
              className={`px-3 py-1.5 rounded text-xs font-bold transition-all flex items-center gap-1.5 ${
                provider === 'claude' && !isCompareMode
                  ? 'bg-[#FF8A00] text-black shadow-[0_0_10px_rgba(255,138,0,0.4)]'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <span>Claude 3.5</span>
            </button>
            <button
              onClick={() => { setProvider('gemini'); setIsCompareMode(false); }}
              className={`px-3 py-1.5 rounded text-xs font-bold transition-all flex items-center gap-1.5 ${
                provider === 'gemini' && !isCompareMode
                  ? 'bg-[#3B82F6] text-white shadow-[0_0_10px_rgba(59,130,246,0.4)]'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <span>Gemini 1.5</span>
            </button>
            <button
              onClick={() => setIsCompareMode(!isCompareMode)}
              className={`px-3 py-1.5 rounded text-xs font-bold transition-all flex items-center gap-1.5 ${
                isCompareMode
                  ? 'bg-purple-600 text-white shadow-[0_0_10px_rgba(168,85,247,0.4)]'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Columns className="w-3.5 h-3.5" />
              <span>Side-by-Side</span>
            </button>
          </div>

          {/* RAG Toggle */}
          <button
            onClick={() => setUseRAG(!useRAG)}
            className={`px-3 py-1.5 rounded-lg border text-xs font-medium flex items-center gap-1.5 transition-colors ${
              useRAG
                ? 'border-emerald-500/50 bg-emerald-500/10 text-emerald-400'
                : 'border-[#252936] text-slate-500 hover:text-slate-300'
            }`}
          >
            <Database className="w-3.5 h-3.5" />
            <span>RAG Context: {useRAG ? 'ON' : 'OFF'}</span>
          </button>

          {/* Blue Team Guardrail Toggle */}
          <button
            onClick={() => setApplyGuardrails(!applyGuardrails)}
            className={`px-3 py-1.5 rounded-lg border text-xs font-medium flex items-center gap-1.5 transition-colors ${
              applyGuardrails
                ? 'border-[#FF8A00]/50 bg-[#FF8A00]/10 text-[#FF8A00]'
                : 'border-[#252936] text-slate-500 hover:text-slate-300'
            }`}
          >
            <Shield className="w-3.5 h-3.5" />
            <span>Blue Team Guardrails: {applyGuardrails ? 'ACTIVE' : 'OFF'}</span>
          </button>
        </div>

        {/* Actions */}
        <div className="flex items-center space-x-2">
          <button
            onClick={handleClearChat}
            className="p-2 rounded-lg bg-[#0E1015] border border-[#252936] text-slate-400 hover:text-white transition-colors"
            title="Reset Chat"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={handleExportChat}
            className="p-2 rounded-lg bg-[#0E1015] border border-[#252936] text-slate-400 hover:text-white transition-colors"
            title="Export JSON"
          >
            <Download className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Main Chat / Side-by-Side Body */}
      <div className="flex-1 bg-[#14161D] border border-[#232736] rounded-xl overflow-y-auto p-6 space-y-4 shadow-inner">
        {isCompareMode && comparisonResult ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">
            {/* Claude Box */}
            <div className="bg-[#0E1015] border border-[#FF8A00]/40 rounded-xl p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between border-b border-[#252936] pb-3 mb-4">
                  <span className="text-sm font-bold text-[#FF8A00] flex items-center gap-2">
                    Claude 3.5 Sonnet
                  </span>
                  <div className="text-[11px] text-slate-400 flex items-center gap-3">
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {comparisonResult.claude_result?.latency_ms}ms</span>
                    <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> {comparisonResult.claude_result?.tokens_used} tokens</span>
                  </div>
                </div>
                <div className="text-sm text-slate-200 whitespace-pre-wrap leading-relaxed">
                  {comparisonResult.claude_result?.response}
                </div>
              </div>
            </div>

            {/* Gemini Box */}
            <div className="bg-[#0E1015] border border-blue-500/40 rounded-xl p-5 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between border-b border-[#252936] pb-3 mb-4">
                  <span className="text-sm font-bold text-blue-400 flex items-center gap-2">
                    Gemini 1.5 Flash
                  </span>
                  <div className="text-[11px] text-slate-400 flex items-center gap-3">
                    <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {comparisonResult.gemini_result?.latency_ms}ms</span>
                    <span className="flex items-center gap-1"><Cpu className="w-3 h-3" /> {comparisonResult.gemini_result?.tokens_used} tokens</span>
                  </div>
                </div>
                <div className="text-sm text-slate-200 whitespace-pre-wrap leading-relaxed">
                  {comparisonResult.gemini_result?.response}
                </div>
              </div>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div
                className={`max-w-3xl rounded-2xl p-4 text-sm leading-relaxed shadow-lg ${
                  msg.role === 'user'
                    ? 'bg-[#1E2330] border border-[#2F3547] text-white'
                    : msg.guardrail_flagged
                    ? 'bg-red-950/20 border border-red-500/40 text-red-200'
                    : 'bg-[#0E1015] border border-[#232736] text-slate-200'
                }`}
              >
                {msg.guardrail_flagged && (
                  <div className="flex items-center gap-2 text-xs font-bold text-red-400 mb-2 pb-2 border-b border-red-500/20">
                    <AlertTriangle className="w-4 h-4" />
                    <span>DEFENSIVE GUARDRAIL INTERCEPTED ACTION</span>
                  </div>
                )}

                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Citations / RAG sources */}
                {msg.rag_sources && msg.rag_sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-[#1F2432] space-y-1">
                    <p className="text-[11px] font-bold text-emerald-400 flex items-center gap-1">
                      <Database className="w-3 h-3" /> RAG Knowledge Retrieved:
                    </p>
                    {msg.rag_sources.map((s, sIdx) => (
                      <div key={sIdx} className="text-[10px] text-slate-400 bg-[#14161D] px-2 py-1 rounded">
                        • {s.document_name} (Relevance: {s.similarity_score})
                      </div>
                    ))}
                  </div>
                )}

                {/* Latency & Token Badges */}
                {msg.role === 'assistant' && (
                  <div className="mt-2.5 flex items-center justify-end space-x-3 text-[10px] text-slate-500">
                    {msg.latency_ms !== undefined && <span>{msg.latency_ms}ms</span>}
                    {msg.tokens_used !== undefined && <span>{msg.tokens_used} tokens</span>}
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="flex items-center space-x-2 text-slate-400 text-xs py-2">
            <span className="w-2 h-2 rounded-full bg-[#FF8A00] animate-ping" />
            <span>Consulting {isCompareMode ? 'both models concurrently' : provider}...</span>
          </div>
        )}
      </div>

      {/* Input Form */}
      <div className="relative">
        <textarea
          rows={2}
          value={inputPrompt}
          onChange={(e) => setInputPrompt(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSendMessage();
            }
          }}
          placeholder={
            isCompareMode
              ? 'Enter prompt to test side-by-side resilience in Claude & Gemini...'
              : `Message ${provider === 'claude' ? 'Claude 3.5 Sonnet' : 'Gemini 1.5 Flash'} (or test an attack payload)...`
          }
          className="w-full bg-[#14161D] border border-[#232736] text-white rounded-xl p-3 pr-24 text-sm focus:outline-none focus:border-[#FF8A00] transition-colors resize-none placeholder-slate-500"
        />

        <button
          onClick={handleSendMessage}
          disabled={loading || !inputPrompt.trim()}
          className="absolute right-3 bottom-4 px-4 py-2 rounded-lg bg-[#FF8A00] hover:bg-[#FFA333] text-black font-bold text-xs flex items-center gap-1.5 transition-colors disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_12px_rgba(255,138,0,0.3)]"
        >
          <Send className="w-3.5 h-3.5" />
          <span>Send</span>
        </button>
      </div>
    </div>
  );
};
