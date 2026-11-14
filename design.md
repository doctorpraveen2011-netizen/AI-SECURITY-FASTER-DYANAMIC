# Design System & UI Specification
## AI SECURITY FASTER – Operations Center

### 1. Aesthetic Direction & Brand Identity
- **Visual Tone**: Modern, high-security cybersecurity Operations Center (SOC) combined with a high-performance LeetCode-inspired developer aesthetic.
- **Palette**:
  - **Background (Canvas)**: `#0A0A0C` (Absolute deep obsidian black)
  - **Surface / Card Background**: `#14161D` / `#161922` (Dark charcoal with subtle border)
  - **Card Hover / Elevation**: `#1C1F2B`
  - **Primary Accent**: `#FF8A00` (Electric Amber / Neon Orange)
  - **Primary Glow**: `rgba(255, 138, 0, 0.25)` to `rgba(255, 138, 0, 0.4)`
  - **Secondary Accents**:
    - Danger / Vulnerability: `#EF4444` (Vibrant Red)
    - Success / Mitigated: `#10B981` (Emerald Green)
    - Info / Scan Time: `#8B5CF6` (Vivid Purple)
    - Cyan / MCP / Agent: `#06B6D4` (Cyan Blue)
  - **Typography**:
    - Primary Text: `#FFFFFF` (Pure White)
    - Secondary Text: `#94A3B8` (Slate 400)
    - Muted / Disabled: `#64748B` (Slate 500)
    - Font Family: `Inter`, `JetBrains Mono` for code/payloads/prompts

### 2. Component Design Specifications

#### 2.1 Navigation Sidebar (Left)
- **Brand Header**:
  - Shield emblem containing letter "A" in vibrant glowing orange.
  - Heading: "AI SECURITY FASTER" (Two lines, bold uppercase, letter-spacing).
- **Navigation Links**:
  - Icon + Text with subtle orange indicator pill on active state.
  - Hover: Background tint `rgba(255, 138, 0, 0.1)` with orange icon glow.
  - Routes:
    1. Overview (Home / Dashboard)
    2. LLM Playground
    3. AI Agent Lab
    4. Attack Testing
    5. OWASP Risk Matrix
    6. MCP Security Lab
    7. Blue Team Mitigations
    8. Before/After Analysis
    9. Wazuh Integration
    10. Reports
    11. Audit Logs
    12. Settings
- **Footer**:
  - "Powered by OWASP" badge with global security compass icon.

#### 2.2 Top Header
- **Search Bar**: Full rounded input with search icon, placeholder: `"Search attacks, risks, or results..."`.
- **Model Selector Toggle**:
  - Claude button with Anthropic sunburst logo.
  - Gemini button with Google multicolour/blue 'G' logo.
  - Active model highlighted with amber border and indicator dot.
- **System Online Indicator**: Glowing green dot with text "System Online".
- **User Avatar**: Circular charcoal avatar badge with initial "P".

#### 2.3 Dashboard Hero Banner
- Glowing shield with lock icon.
- Title: `Welcome to AI Security Faster` (White bold text).
- Subtitle: `Automated Red-Teaming & Blue-Teaming for LLMs and AI Agents` (Slate 400).
- Tagline on right: `Test • Detect • Mitigate • Stay Secure` (Glowing orange dots).
- Visual: Glowing 3D neural brain network visualization in neon orange vector graphics.

#### 2.4 Metric Cards (Top Row)
1. **Total Tests Run**:
   - Number: `48` (or dynamic), trend `↑+12%` (Orange badge), orange sparkline line.
2. **Vulnerabilities Found**:
   - Number: `27`, trend `↑+8%` (Red badge), warning triangle icon, red sparkline.
3. **Mitigated Risks**:
   - Number: `24`, trend `↑+15%` (Green badge), green shield check icon, green sparkline.
4. **Avg Scan Time**:
   - Number: `2m 14s`, purple clock icon, purple sparkline.

#### 2.5 Models & Tools Card
- Left section: Model selection pills (Claude, Gemini) with active status indicators.
- Right section: Agent Tools badge list:
  - `File Read`, `Email`, `HTTP Call`, `MCP Tools`.

#### 2.6 Risk Coverage Card (OWASP 2026)
- Pill switch: `LLM Top 10` | `Agentic Top 10`.
- Risk tags with orange bullet indicators:
  - LLM: `LLM01: Prompt Injection`, `LLM02: Sensitive Info`, `LLM08: Excessive Agency`, `LLM10: Vector Misuse`.
  - Agentic: `ASI01: Jailbreak Agents`, `ASI02: Tool Misuse`, `ASI03: Goal Misalignment`, `ASI05: Data Leakage`, `ASI06: Privilege Escalation`.

#### 2.7 Attack Test Cases Card
- Expandable list of vulnerability categories:
  - `LLM01 Prompt Injection` (3+ Tests)
  - `LLM02 Sensitive Information` (3+ Tests)
  - `LLM03 Supply Chain Attacks` (3+ Tests)
  - `LLM08 Excessive Agency` (3+ Tests)
  - `LLM10 Vector Misuse` (3+ Tests)
- Dual-provider progress bars:
  - Claude: `3/3 ✓` with amber status bar.
  - Gemini: `3/3 ✓` with amber status bar.

#### 2.8 Mitigation Results Card
- Header with green button: `All Mitigations Applied ✓`.
- Table columns:
  - Risk category
  - Before Mitigation: e.g. `High Risk (87%)` (Red badge)
  - Arrow: `→`
  - After Mitigation: e.g. `Low Risk (12%)` (Green badge)

#### 2.9 MCP Connection Risk Card
- Status banner: Shield icon, `Connection Secure`, `Risk Score: 11%` (Emerald green).
- PoC result text: `"POC Result: Attempted path traversal (../../../etc/shadow) blocked."`.
- Actions: `Blocked` green badge, `View Details →` button.

#### 2.10 Test Reports Card
- Recharts Dual-Line Chart: Vulnerabilities (Orange `#FF8A00`) vs Mitigated (Green `#10B981`) across weekdays.
- Action: Glowing orange `Download Report` button with download tray icon.
- Last scan timestamp: `Last Scan: Nov 12, 2026 • 19:45`.
