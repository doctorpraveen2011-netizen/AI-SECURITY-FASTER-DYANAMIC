import React from 'react';
import { Search, ShieldAlert, CheckCircle2 } from 'lucide-react';

interface HeaderProps {
  currentProvider: 'claude' | 'gemini';
  onProviderChange: (provider: 'claude' | 'gemini') => void;
  systemOnline?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  currentProvider,
  onProviderChange,
  systemOnline = true,
}) => {
  return (
    <header className="h-16 border-b border-[#1E222D] bg-[#0A0A0C] px-6 flex items-center justify-between sticky top-0 z-40">
      {/* Search Input */}
      <div className="relative w-96">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
        <input
          type="text"
          placeholder="Search attacks, risks, or results..."
          className="w-full bg-[#14161D] border border-[#252936] text-sm text-white placeholder-slate-500 rounded-full pl-10 pr-4 py-2 focus:outline-none focus:border-[#FF8A00] transition-colors"
        />
      </div>

      {/* Right Controls: Model Selectors, Online Status, Profile */}
      <div className="flex items-center space-x-4">
        {/* Model Switcher Pills */}
        <div className="flex items-center space-x-2 bg-[#14161D] p-1 rounded-xl border border-[#252936]">
          {/* Claude Pill */}
          <button
            onClick={() => onProviderChange('claude')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              currentProvider === 'claude'
                ? 'bg-[#1E222D] text-white border border-[#FF8A00] shadow-[0_0_12px_rgba(255,138,0,0.3)]'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            {/* Anthropic Sunburst Icon */}
            <svg className="w-4 h-4 text-[#FF8A00]" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2l1.5 5.5L19 9l-5.5 1.5L12 16l-1.5-5.5L5 9l5.5-1.5z" />
              <circle cx="12" cy="12" r="3" fill="#FF8A00" />
            </svg>
            <span>Claude</span>
            <span className="text-[10px] text-slate-400">⌄</span>
          </button>

          {/* Gemini Pill */}
          <button
            onClick={() => onProviderChange('gemini')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              currentProvider === 'gemini'
                ? 'bg-[#1E222D] text-white border border-[#3B82F6] shadow-[0_0_12px_rgba(59,130,246,0.3)]'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            {/* Google G icon */}
            <span className="w-4 h-4 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-[11px]">
              G
            </span>
            <span>Gemini</span>
            <span className="text-[10px] text-slate-400">⌄</span>
          </button>
        </div>

        {/* System Online Status */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-[#14161D] border border-[#252936]">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_#10B981]" />
          <span className="text-xs font-medium text-slate-200">System Online</span>
        </div>

        {/* User Profile Avatar */}
        <div className="w-8 h-8 rounded-full bg-[#202430] border border-[#303544] flex items-center justify-center text-sm font-bold text-white shadow-sm hover:border-[#FF8A00] cursor-pointer transition-colors">
          P
        </div>
      </div>
    </header>
  );
};
