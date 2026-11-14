import React from 'react';
import {
  LayoutDashboard,
  MessageSquare,
  Bot,
  Crosshair,
  Grid,
  Cpu,
  ShieldCheck,
  GitCompare,
  Network,
  FileText,
  History,
  Settings,
  Shield
} from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onTabChange }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'playground', label: 'LLM Chat', icon: MessageSquare },
    { id: 'agent-lab', label: 'AI Agent', icon: Bot },
    { id: 'attack-testing', label: 'Attack Tests', icon: Crosshair },
    { id: 'owasp-matrix', label: 'OWASP Matrix', icon: Grid },
    { id: 'mcp-lab', label: 'MCP Connector', icon: Cpu },
    { id: 'mitigations', label: 'Mitigations', icon: ShieldCheck },
    { id: 'before-after', label: 'Before / After', icon: GitCompare },
    { id: 'wazuh', label: 'Integrations', icon: Network },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'audit-logs', label: 'Audit Logs', icon: History },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#0A0A0C] border-r border-[#1E222D] flex flex-col justify-between h-screen sticky top-0 select-none z-50">
      {/* Brand Header */}
      <div>
        <div className="p-6 flex items-center space-x-3 cursor-pointer" onClick={() => onTabChange('overview')}>
          {/* Glowing Shield Logo Emblem */}
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#FF8A00] to-[#B35F00] flex items-center justify-center shadow-[0_0_18px_rgba(255,138,0,0.5)]">
            <span className="font-extrabold text-black text-xl tracking-tighter">A</span>
          </div>
          <div>
            <h1 className="text-sm font-black tracking-wider text-white uppercase font-sans">
              AI SECURITY
            </h1>
            <p className="text-xs font-black tracking-widest text-[#FF8A00] uppercase font-sans">
              FASTER
            </p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="px-3 space-y-1 mt-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all group ${
                  isActive
                    ? 'bg-gradient-to-r from-[#FF8A00]/20 to-transparent text-[#FF8A00] border-l-2 border-[#FF8A00] font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-[#14161D]'
                }`}
              >
                <Icon
                  className={`w-4 h-4 transition-transform group-hover:scale-110 ${
                    isActive ? 'text-[#FF8A00] drop-shadow-[0_0_8px_rgba(255,138,0,0.6)]' : 'text-slate-400'
                  }`}
                />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer: Powered by OWASP */}
      <div className="p-4 border-t border-[#181B24]">
        <div className="flex items-center space-x-2.5 px-3 py-2 rounded-lg bg-[#12141A] border border-[#202430]">
          <div className="w-6 h-6 rounded-full bg-slate-800 flex items-center justify-center">
            <Shield className="w-3.5 h-3.5 text-slate-300" />
          </div>
          <div>
            <p className="text-[10px] text-slate-400 font-medium">Powered by</p>
            <p className="text-xs font-bold text-slate-200 tracking-wider">OWASP</p>
          </div>
        </div>
      </div>
    </aside>
  );
};
