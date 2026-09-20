import asyncio
from playwright.async_api import async_playwright
import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RailBlock-AI B&W Architecture Perfect Layout</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800;900&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            width: 1840px;
            background-color: #ffffff;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0;
        }

        /* MAIN CONTAINER - FIXED EXACT CANVA SLIDE DIMENSIONS */
        .main-content {
            width: 1840px;
            padding: 20px 24px;
            display: flex;
            gap: 28px;
            background: #ffffff;
            position: relative;
        }

        /* LEFT SIDE: PLATFORM ARCHITECTURE (64%) */
        .left-panel {
            flex: 1.8;
            display: flex;
            flex-direction: column;
            gap: 10px;
            position: relative;
        }

        .panel-title {
            font-size: 28px;
            font-weight: 900;
            color: #000000;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border-left: 8px solid #000000;
            padding-left: 14px;
            line-height: 1.0;
            margin-bottom: 4px;
        }

        /* ROW 1: USER PORTALS */
        .portals-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            position: relative;
        }

        .portal-card {
            background: #ffffff;
            border: 3px solid #000000;
            border-radius: 12px;
            padding: 12px 10px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            height: 175px;
        }

        .portal-card .card-icon {
            font-size: 26px;
            margin-bottom: 2px;
        }

        .portal-card .card-title {
            font-size: 17.5px;
            font-weight: 800;
            color: #000000;
            margin-bottom: 4px;
            line-height: 1.25;
        }

        .portal-card .card-badge {
            display: inline-block;
            background: #EAEAEA;
            color: #000000;
            border: 1.5px solid #000000;
            font-size: 12.5px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 6px;
            margin-bottom: 6px;
            align-self: center;
        }

        .portal-card .card-desc {
            font-size: 13.5px;
            font-weight: 600;
            color: #1A1A1A;
            line-height: 1.35;
        }

        /* PERFECT ALIGNED CONNECTOR ARROWS (ROW 1 TO ENGINE) */
        .arrows-row-top {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            height: 16px;
            align-items: center;
        }

        .arrow-center-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .arrow-down {
            width: 0;
            height: 0;
            border-left: 10px solid transparent;
            border-right: 10px solid transparent;
            border-top: 14px solid #000000;
        }

        /* MIDDLE ENGINE LAYER */
        .engine-box {
            background: #F9F9F9;
            border: 4px solid #000000;
            border-radius: 16px;
            padding: 16px 20px;
            text-align: center;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
            position: relative;
        }

        .engine-title {
            font-size: 30px;
            font-weight: 900;
            color: #000000;
            letter-spacing: 1px;
            margin-bottom: 2px;
        }

        .engine-subtitle {
            font-size: 16.5px;
            font-weight: 700;
            color: #222222;
            margin-bottom: 10px;
        }

        .engine-pills {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px 10px;
        }

        .engine-pill {
            background: #ffffff;
            border: 2px solid #000000;
            color: #000000;
            font-size: 14px;
            font-weight: 800;
            padding: 5px 14px;
            border-radius: 20px;
        }

        /* PERFECT ALIGNED CONNECTOR ARROWS (ENGINE TO ROW 3) */
        .arrows-row-bottom {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            height: 16px;
            align-items: center;
        }

        /* ROW 3: BACKEND SERVICES */
        .backend-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            position: relative;
        }

        .backend-card {
            background: #ffffff;
            border: 3px solid #000000;
            border-radius: 12px;
            padding: 14px 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            height: 185px;
            position: relative;
        }

        .backend-card .card-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }

        .backend-card .card-icon {
            font-size: 24px;
        }

        .backend-card .card-title {
            font-size: 18.5px;
            font-weight: 800;
            color: #000000;
        }

        .backend-card .card-tech {
            font-size: 13.5px;
            font-weight: 800;
            color: #000000;
            margin-bottom: 6px;
            background: #F0F0F0;
            padding: 2px 8px;
            border-radius: 4px;
            display: inline-block;
            align-self: flex-start;
        }

        .backend-card .card-desc {
            font-size: 13.5px;
            font-weight: 600;
            color: #1A1A1A;
            line-height: 1.38;
        }

        /* CLEAN PROTOTYPE BADGE INTEGRATED AT BOTTOM RIGHT OF 3RD CARD */
        .prototype-badge-inline {
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 6px;
            margin-top: auto;
            padding-top: 4px;
        }

        .prototype-badge-label {
            font-size: 13.5px;
            font-weight: 900;
            color: #000000;
        }

        .prototype-badge-bubble {
            background: #000000;
            color: #ffffff;
            border-radius: 6px;
            padding: 3px 10px;
            font-size: 13px;
            font-weight: 900;
            letter-spacing: 0.5px;
        }

        /* RIGHT SIDE: BLOCK PLANNING RULE (36%) */
        .right-panel {
            flex: 1.05;
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding-left: 18px;
            border-left: 3px dashed #CCCCCC;
        }

        .rule-cards {
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin-top: 4px;
        }

        .rule-card {
            display: flex;
            gap: 14px;
            align-items: flex-start;
            background: #ffffff;
            border: 3px solid #000000;
            border-radius: 12px;
            padding: 14px 14px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            height: 138px;
        }

        .rule-number {
            width: 44px;
            height: 44px;
            background: #000000;
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 900;
            flex-shrink: 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }

        .rule-content {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .rule-title {
            font-size: 18.5px;
            font-weight: 900;
            color: #000000;
            letter-spacing: 0.5px;
        }

        .rule-desc {
            font-size: 14px;
            font-weight: 600;
            color: #1A1A1A;
            line-height: 1.35;
        }
    </style>
</head>
<body>

    <!-- MAIN CONTAINER ONLY -->
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
                    <div class="card-desc">Real-time track topology, live train feeds & 1-click block approval workflow.</div>
                </div>

                <div class="portal-card">
                    <div class="card-icon">📱</div>
                    <div class="card-title">Departmental App</div>
                    <div class="card-badge">React Native</div>
                    <div class="card-desc">Field app for P-Way, TRD & S&T teams to log maintenance block requests.</div>
                </div>

                <div class="portal-card">
                    <div class="card-icon">⚡</div>
                    <div class="card-title">AI Dispatcher Console</div>
                    <div class="card-badge">React Web</div>
                    <div class="card-desc">Monitors live train speeds, priority queues & loop line overtake directives.</div>
                </div>

                <div class="portal-card">
                    <div class="card-icon">🏛️</div>
                    <div class="card-title">CRIS System Gateway</div>
                    <div class="card-badge">React Web</div>
                    <div class="card-desc">Bi-directional sync with COA (Control Office) & BDMS railway systems.</div>
                </div>
            </div>

            <!-- PERFECT ALIGNED CONNECTOR ARROWS (ROW 1 TO ENGINE) -->
            <div class="arrows-row-top">
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
            </div>

            <!-- MIDDLE ENGINE LAYER -->
            <div class="engine-box">
                <div class="engine-title">RAILBLOCK-AI CORE ENGINE</div>
                <div class="engine-subtitle">Core Optimization & Execution Layer (FastAPI + Python)</div>
                <div class="engine-pills">
                    <span class="engine-pill">REST & WebSockets</span>
                    <span class="engine-pill">MILP Solver Algorithm</span>
                    <span class="engine-pill">Joint Block Consolidation</span>
                    <span class="engine-pill">Spatio-Temporal Graph Engine</span>
                    <span class="engine-pill">CRIS System Sync</span>
                </div>
            </div>

            <!-- PERFECT ALIGNED CONNECTOR ARROWS (ENGINE TO ROW 3) -->
            <div class="arrows-row-bottom">
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
                <div class="arrow-center-wrapper"><div class="arrow-down"></div></div>
            </div>

            <!-- ROW 3: BACKEND SERVICES -->
            <div class="backend-grid">
                <div class="backend-card">
                    <div class="card-header">
                        <span class="card-icon">🧠</span>
                        <span class="card-title">AI Service</span>
                    </div>
                    <div class="card-tech">Google OR-Tools, PuLP</div>
                    <div class="card-desc">Solves MILP matrix to group overlapping P-Way, TRD & S&T requests into joint windows.</div>
                </div>

                <div class="backend-card">
                    <div class="card-header">
                        <span class="card-icon">🗄️</span>
                        <span class="card-title">Data & Spatial Layer</span>
                    </div>
                    <div class="card-tech">PostgreSQL + PostGIS</div>
                    <div class="card-desc">Track spatial graphs, Redis telemetry cache & uptime analytics.</div>
                </div>

                <div class="backend-card">
                    <div class="card-header">
                        <span class="card-icon">🔗</span>
                        <span class="card-title">Railway Integrations</span>
                    </div>
                    <div class="card-tech">CRIS Open APIs, WebSockets</div>
                    <div class="card-desc">Automated COA & BDMS REST streams with Human-in-the-Loop approval.</div>
                    
                    <!-- CLEAN INLINE PROTOTYPE BADGE -->
                    <div class="prototype-badge-inline">
                        <span class="prototype-badge-label">Prototype ➔</span>
                        <span class="prototype-badge-bubble">WEBSITE</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- RIGHT PANEL: BLOCK PLANNING RULE -->
        <div class="right-panel">
            <div class="panel-title">MILP BLOCK PLANNING RULE</div>

            <div class="rule-cards">
                <div class="rule-card">
                    <div class="rule-number">1</div>
                    <div class="rule-content">
                        <div class="rule-title">FILTER & CONSOLIDATE</div>
                        <div class="rule-desc">Groups overlapping P-Way, TRD & S&T requests into a single joint window, preventing repeated track closures.</div>
                    </div>
                </div>

                <div class="rule-card">
                    <div class="rule-number">2</div>
                    <div class="rule-content">
                        <div class="rule-title">RANK & SOLVE (MILP)</div>
                        <div class="rule-desc">Executes MILP solver to minimize train delays, prioritizing express traffic over freight trains.</div>
                    </div>
                </div>

                <div class="rule-card">
                    <div class="rule-number">3</div>
                    <div class="rule-content">
                        <div class="rule-title">DYNAMIC DISPATCH</div>
                        <div class="rule-desc">Spatio-temporal graph engine dispatches loop line overtakes with zero domino delay.</div>
                    </div>
                </div>
            </div>
        </div>

    </div>

</body>
</html>
"""

with open("slide3_perfect_layout.html", "w") as f:
    f.write(html_content)

print("Saved slide3_perfect_layout.html")
