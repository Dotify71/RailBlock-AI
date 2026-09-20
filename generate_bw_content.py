import asyncio
from playwright.async_api import async_playwright
import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RailBlock-AI Architecture Content Only (Black & White)</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            width: 1920px;
            background-color: #ffffff;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        /* MAIN CONTENT AREA ONLY - NO HEADER / NO FOOTER */
        .main-content {
            width: 1880px;
            padding: 30px 40px;
            display: flex;
            gap: 40px;
            background: #ffffff;
            position: relative;
        }

        /* LEFT SIDE: PLATFORM ARCHITECTURE (65%) */
        .left-panel {
            flex: 1.85;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .panel-title {
            font-size: 26px;
            font-weight: 800;
            color: #1A1A1A;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border-left: 6px solid #1A1A1A;
            padding-left: 14px;
            line-height: 1.1;
        }

        /* ROW 1: USER PORTALS */
        .portals-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }

        .portal-card {
            background: #ffffff;
            border: 2px solid #1A1A1A;
            border-radius: 12px;
            padding: 16px 14px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 170px;
        }

        .portal-card .card-icon {
            font-size: 24px;
            margin-bottom: 2px;
        }

        .portal-card .card-title {
            font-size: 16px;
            font-weight: 700;
            color: #1A1A1A;
            margin-bottom: 4px;
        }

        .portal-card .card-badge {
            display: inline-block;
            background: #F0F0F0;
            color: #1A1A1A;
            border: 1px solid #CCCCCC;
            font-size: 11.5px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 6px;
            margin-bottom: 6px;
        }

        .portal-card .card-desc {
            font-size: 12.5px;
            color: #4A4A4A;
            line-height: 1.35;
        }

        /* CONNECTOR ARROWS */
        .arrows-row {
            display: flex;
            justify-content: space-around;
            padding: 0 40px;
            margin: -6px 0;
        }

        .arrow-down {
            width: 0;
            height: 0;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-top: 14px solid #1A1A1A;
        }

        /* MIDDLE ENGINE LAYER */
        .engine-box {
            background: #FAFAFA;
            border: 3px solid #1A1A1A;
            border-radius: 16px;
            padding: 20px 24px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            position: relative;
        }

        .engine-title {
            font-size: 28px;
            font-weight: 800;
            color: #1A1A1A;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }

        .engine-subtitle {
            font-size: 16px;
            font-weight: 600;
            color: #333333;
            margin-bottom: 14px;
        }

        .engine-pills {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px 14px;
        }

        .engine-pill {
            background: #ffffff;
            border: 2px solid #1A1A1A;
            color: #1A1A1A;
            font-size: 13px;
            font-weight: 700;
            padding: 6px 16px;
            border-radius: 20px;
        }

        /* ROW 3: BACKEND SERVICES */
        .backend-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }

        .backend-card {
            background: #ffffff;
            border: 2px solid #1A1A1A;
            border-radius: 12px;
            padding: 18px 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            height: 195px;
        }

        .backend-card .card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
        }

        .backend-card .card-icon {
            font-size: 24px;
        }

        .backend-card .card-title {
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A;
        }

        .backend-card .card-tech {
            font-size: 13.5px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 8px;
        }

        .backend-card .card-desc {
            font-size: 13px;
            color: #4A4A4A;
            line-height: 1.4;
        }

        /* PROTOTYPE CALLOUT CLOUD */
        .prototype-callout {
            position: absolute;
            bottom: 40px;
            left: 55%;
            display: flex;
            align-items: center;
            gap: 12px;
            z-index: 10;
        }

        .prototype-label {
            font-size: 17px;
            font-weight: 800;
            color: #1A1A1A;
        }

        .cloud-bubble {
            background: #ffffff;
            border: 3px solid #1A1A1A;
            border-radius: 30px;
            padding: 10px 24px;
            color: #1A1A1A;
            font-size: 18px;
            font-weight: 800;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* RIGHT SIDE: BLOCK PLANNING RULE (35%) */
        .right-panel {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding-left: 20px;
            border-left: 2px dashed #CCCCCC;
        }

        .rule-cards {
            display: flex;
            flex-direction: column;
            gap: 24px;
            margin-top: 10px;
        }

        .rule-card {
            display: flex;
            gap: 18px;
            align-items: flex-start;
        }

        .rule-number {
            width: 48px;
            height: 48px;
            background: #1A1A1A;
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 800;
            flex-shrink: 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }

        .rule-content {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .rule-title {
            font-size: 19px;
            font-weight: 800;
            color: #1A1A1A;
            letter-spacing: 0.5px;
        }

        .rule-desc {
            font-size: 14px;
            color: #4A4A4A;
            line-height: 1.45;
        }
    </style>
</head>
<body>

    <!-- MAIN CONTENT ONLY (NO HEADER BANNER, NO FOOTER BANNER) -->
    <div class="main-content">

        <!-- LEFT PANEL: PLATFORM ARCHITECTURE -->
        <div class="left-panel">
            <div class="panel-title">PLATFORM ARCHITECTURE</div>

            <!-- ROW 1: USER PORTALS -->
            <div class="portals-grid">
                <div class="portal-card">
                    <div class="card-icon">🖥️</div>
                    <div class="card-title">Section Controller App</div>
                    <div class="card-badge">React Web</div>
                    <div class="card-desc">Real-time section track overview & automated block approval workflow.</div>
                </div>

                <div class="portal-card">
                    <div class="card-icon">📱</div>
                    <div class="card-title">Departmental App</div>
                    <div class="card-badge">React Native</div>
                    <div class="card-desc">P-Way, TRD & S&T field engineers submit maintenance block requests.</div>
                </div>

                <div class="portal-card">
                    <div class="card-icon">⚡</div>
                    <div class="card-title">AI Dispatcher Console</div>
                    <div class="card-badge">React Web</div>
                    <div class="card-desc">Live train telemetry feeds, speed priority & loop line overtake directives.</div>
                </div>

                <div class="portal-card">
                    <div class="card-icon">🏛️</div>
                    <div class="card-title">CRIS System Gateway</div>
                    <div class="card-badge">React Web</div>
                    <div class="card-desc">COA & BDMS system feeds integration & controller approval sync.</div>
                </div>
            </div>

            <!-- CONNECTOR ARROWS -->
            <div class="arrows-row">
                <div class="arrow-down"></div>
                <div class="arrow-down"></div>
                <div class="arrow-down"></div>
                <div class="arrow-down"></div>
            </div>

            <!-- MIDDLE ENGINE LAYER -->
            <div class="engine-box">
                <div class="engine-title">RAILBLOCK-AI CORE ENGINE</div>
                <div class="engine-subtitle">Application & Optimization Layer (Python FastAPI + MILP Solver)</div>
                <div class="engine-pills">
                    <span class="engine-pill">REST & WebSockets</span>
                    <span class="engine-pill">MILP Constraint Solver</span>
                    <span class="engine-pill">Joint Maintenance Window Consolidation</span>
                    <span class="engine-pill">Spatio-Temporal Graph Engine</span>
                    <span class="engine-pill">CRIS COA / BDMS Sync</span>
                </div>
            </div>

            <!-- CONNECTOR ARROWS -->
            <div class="arrows-row" style="margin-top: -2px;">
                <div class="arrow-down"></div>
                <div class="arrow-down"></div>
                <div class="arrow-down"></div>
            </div>

            <!-- ROW 3: BACKEND SERVICES -->
            <div class="backend-grid">
                <div class="backend-card">
                    <div class="card-header">
                        <span class="card-icon">🧠</span>
                        <span class="card-title">AI Service</span>
                    </div>
                    <div class="card-tech">Google OR-Tools, PuLP</div>
                    <div class="card-desc">MILP constraint solver algorithm grouping overlapping track section requests across P-Way, TRD & S&T.</div>
                </div>

                <div class="backend-card">
                    <div class="card-header">
                        <span class="card-icon">🗄️</span>
                        <span class="card-title">Data & Spatial Layer</span>
                    </div>
                    <div class="card-tech">PostgreSQL + PostGIS</div>
                    <div class="card-desc">Spatial track network topology, Redis telemetry cache, NumPy downtime & section capacity formulas.</div>
                </div>

                <div class="backend-card">
                    <div class="card-header">
                        <span class="card-icon">🔗</span>
                        <span class="card-title">Railway Integrations</span>
                    </div>
                    <div class="card-tech">CRIS Open APIs, WebSocket</div>
                    <div class="card-desc">COA (Control Office) & BDMS sync, automated controller click approval workflow & telemetry stream.</div>
                </div>
            </div>
        </div>

        <!-- PROTOTYPE CALLOUT CLOUD -->
        <div class="prototype-callout">
            <span class="prototype-label">Prototype ➔</span>
            <div class="cloud-bubble">WEBSITE</div>
        </div>

        <!-- RIGHT PANEL: BLOCK PLANNING RULE -->
        <div class="right-panel">
            <div class="panel-title">MILP BLOCK PLANNING RULE</div>

            <div class="rule-cards">
                <div class="rule-card">
                    <div class="rule-number">1</div>
                    <div class="rule-content">
                        <div class="rule-title">FILTER & CONSOLIDATE</div>
                        <div class="rule-desc">Groups overlapping P-Way, TRD & S&T track section requests into a single 4h joint maintenance window to eliminate repeated section closures.</div>
                    </div>
                </div>

                <div class="rule-card">
                    <div class="rule-number">2</div>
                    <div class="rule-content">
                        <div class="rule-title">RANK & SOLVE (MILP)</div>
                        <div class="rule-desc">Formulates Mixed-Integer Linear Programming to minimize total train delay while prioritizing high-speed express trains over slow freight traffic.</div>
                    </div>
                </div>

                <div class="rule-card">
                    <div class="rule-number">3</div>
                    <div class="rule-content">
                        <div class="rule-title">DYNAMIC DISPATCH</div>
                        <div class="rule-desc">Spatio-temporal graph rerouting dispatches loop line overtakes and dynamically updates section capacity with zero domino delay.</div>
                    </div>
                </div>
            </div>
        </div>

    </div>

</body>
</html>
"""

html_file = "slide3_bw_content.html"
with open(html_file, "w") as f:
    f.write(html_content)

print("Saved slide3_bw_content.html")
