import React, { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardOverview } from './pages/DashboardOverview';
import { LLMPlayground } from './pages/LLMPlayground';
import { AgentLab } from './pages/AgentLab';
import { AttackTesting } from './pages/AttackTesting';
import { OWASPRiskMatrix } from './pages/OWASPRiskMatrix';
import { MCPSecurityLab } from './pages/MCPSecurityLab';
import { BlueTeamMitigations } from './pages/BlueTeamMitigations';
import { BeforeAfterAnalysis } from './pages/BeforeAfterAnalysis';
import { WazuhIntegration } from './pages/WazuhIntegration';
import { ReportsPage } from './pages/ReportsPage';
import { AuditLogs } from './pages/AuditLogs';
import { SettingsPage } from './pages/SettingsPage';

export function App() {
  const [currentTab, setCurrentTab] = useState<string>('overview');
  const [currentProvider, setCurrentProvider] = useState<'claude' | 'gemini'>('claude');

  const renderContent = () => {
    switch (currentTab) {
      case 'overview':
        return (
          <DashboardOverview
            onNavigate={setCurrentTab}
            currentProvider={currentProvider}
            onProviderChange={setCurrentProvider}
          />
        );
      case 'playground':
        return <LLMPlayground />;
      case 'agent-lab':
        return <AgentLab />;
      case 'attack-testing':
        return <AttackTesting />;
      case 'owasp-matrix':
        return <OWASPRiskMatrix />;
      case 'mcp-lab':
        return <MCPSecurityLab />;
      case 'mitigations':
        return <BlueTeamMitigations />;
      case 'before-after':
        return <BeforeAfterAnalysis />;
      case 'wazuh':
        return <WazuhIntegration />;
      case 'reports':
        return <ReportsPage />;
      case 'audit-logs':
        return <AuditLogs />;
      case 'settings':
        return <SettingsPage />;
      default:
        return (
          <DashboardOverview
            onNavigate={setCurrentTab}
            currentProvider={currentProvider}
            onProviderChange={setCurrentProvider}
          />
        );
    }
  };

  return (
    <div className="flex h-screen bg-[#0A0A0C] text-slate-100 overflow-hidden font-sans">
      {/* 1. Left Sidebar (Fixed 64) */}
      <Sidebar currentTab={currentTab} onTabChange={setCurrentTab} />

      {/* 2. Main Content Canvas */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Header */}
        <Header
          currentProvider={currentProvider}
          onProviderChange={setCurrentProvider}
          systemOnline={true}
        />

        {/* Scrollable Page Body */}
        <main className="flex-1 overflow-y-auto">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}

export default App;
