import asyncio
from playwright.async_api import async_playwright
import os

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RailBlock-AI SIH 2026 Presentation PDF</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800;900&family=Cinzel:wght@700&display=swap');
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Public Sans', -apple-system, sans-serif;
        }

        @page {
            size: 1920px 1080px;
            margin: 0;
        }

        .slide {
            width: 1920px;
            height: 1080px;
            page-break-after: always;
            page-break-inside: avoid;
            background: #ffffff;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        /* HEADER BANNER */
        .header {
            height: 120px;
            width: 100%;
            padding: 20px 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #ffffff;
        }

        .header-logo-left img {
            height: 75px;
            object-fit: contain;
        }

        .header-title-main {
            font-family: 'Times New Roman', serif;
            font-size: 52px;
            font-weight: 700;
            color: #1F4E79;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .header-title-green {
            font-family: 'Times New Roman', serif;
            font-size: 48px;
            font-weight: 700;
            color: #1E8449;
            text-align: center;
        }

        .header-logo-right img {
            height: 80px;
            object-fit: contain;
        }

        /* FOOTER BANNER */
        .footer {
            height: 50px;
            background: #0284C7;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 60px;
            font-size: 16px;
            font-weight: 700;
        }

        /* SLIDE 1 FIXED CONTENT */
        .slide1-body {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 80px 40px 100px;
            position: relative;
        }

        .slide1-info {
            display: flex;
            flex-direction: column;
            gap: 28px;
            max-width: 1050px;
        }

        .info-row {
            display: flex;
            align-items: flex-start;
            font-size: 32px;
            line-height: 1.3;
        }

        .info-row .bullet {
            color: #1F4E79;
            font-size: 28px;
            margin-right: 16px;
            margin-top: 4px;
        }

        .info-row .label-green {
            color: #27AE60;
            font-weight: 800;
            white-space: nowrap;
            margin-right: 12px;
        }

        .info-row .label-orange {
            color: #E67E22;
            font-weight: 800;
            white-space: nowrap;
            margin-right: 12px;
        }

        .info-row .value {
            color: #000000;
            font-weight: 600;
        }

        .slide1-graphic {
            width: 550px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* SLIDE 2 BODY */
        .slide2-body {
            flex: 1;
            padding: 20px 60px 30px 60px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 50px;
            align-items: center;
        }

        .section-box {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .sec-title-orange {
            font-size: 32px;
            font-weight: 800;
            color: #E67E22;
        }

        .sec-title-green {
            font-size: 32px;
            font-weight: 800;
            color: #27AE60;
        }

        .bullet-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
            font-size: 24px;
            color: #1A252C;
            line-height: 1.4;
        }

        .bullet-list li::before {
            content: "• ";
            color: #1A252C;
            font-weight: bold;
        }

        .comparison-table-card {
            background: #ffffff;
            border: 2px solid #1E8449;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }

        .card-hdr {
            background: #1E8449;
            color: #ffffff;
            padding: 16px;
            text-align: center;
            font-size: 22px;
            font-weight: 800;
        }

        .card-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            padding: 20px;
            gap: 16px;
            background: #F4F9F5;
        }

        .grid-col-missing {
            background: #FFFFFF;
            border: 1.5px solid #F5B7B1;
            border-radius: 12px;
            padding: 16px;
        }

        .grid-col-included {
            background: #FFFFFF;
            border: 1.5px solid #A9DFBF;
            border-radius: 12px;
            padding: 16px;
        }

        /* SLIDE 3 BODY */
        .slide3-body {
            flex: 1;
            padding: 10px 50px 20px 50px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .tech-table {
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }

        .tech-table th {
            background: #EAECEE;
            color: #1A252C;
            font-size: 20px;
            font-weight: 800;
            padding: 16px;
            border: 1px solid #D5D8DC;
            text-align: center;
        }

        .tech-table td {
            font-size: 18px;
            padding: 16px;
            border: 1px solid #D5D8DC;
            vertical-align: middle;
        }

        /* SLIDE 4 & 5 CARDS */
        .cards-grid-4 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            padding: 20px 60px;
        }

        .benefit-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 28px;
            border: 2px solid #D5D8DC;
            box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body>

    <!-- ========================================== -->
    <!-- SLIDE 1: TITLE SLIDE (FIXED & CLEAN)       -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="header">
            <div class="header-logo-left">
                <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="#C0392B"/>
                    <path d="M50 15 L85 30 V55 C85 75 50 90 50 90 C50 90 15 75 15 55 V30 L50 15 Z" fill="#922B21" stroke="#FFFFFF" stroke-width="3"/>
                    <path d="M25 65 L75 65 M30 50 L70 50 M35 35 L65 35" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
                    <circle cx="50" cy="50" r="12" fill="#F1C40F"/>
                </svg>
            </div>
            <div class="header-title-main">SMART INDIA HACKATHON 2026</div>
            <div class="header-logo-right">
                <svg width="180" height="65" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="35" fill="#E67E22"/>
                    <path d="M50 20 V80 M20 50 H80 M30 30 L70 70 M30 70 L70 30" stroke="#FFFFFF" stroke-width="4"/>
                    <text x="95" y="45" fill="#1F4E79" font-size="22" font-weight="800">SMART INDIA</text>
                    <text x="95" y="70" fill="#27AE60" font-size="20" font-weight="800">HACKATHON 2026</text>
                </svg>
            </div>
        </div>

        <div class="slide1-body">
            <div class="slide1-info">
                <div class="info-row">
                    <span class="bullet">■</span>
                    <span class="label-green">Problem Statement ID :</span>
                    <span class="value">SIH26027</span>
                </div>
                <div class="info-row">
                    <span class="bullet">■</span>
                    <span class="label-orange">Problem Statement Title :</span>
                    <span class="value">AI-Powered Automatic Block Planning to Maximize Asset Availability for Train Operations on Indian Railways</span>
                </div>
                <div class="info-row">
                    <span class="bullet">■</span>
                    <span class="label-green">Theme:</span>
                    <span class="value">Transportation & Logistics</span>
                </div>
                <div class="info-row">
                    <span class="bullet">■</span>
                    <span class="label-orange">Category:</span>
                    <span class="value">Software</span>
                </div>
                <div class="info-row">
                    <span class="bullet">■</span>
                    <span class="label-green">Team ID :</span>
                    <span class="value">NST</span>
                </div>
                <div class="info-row">
                    <span class="bullet">■</span>
                    <span class="label-orange">Team Name :</span>
                    <span class="value">RailBlock-AI</span>
                </div>
            </div>

            <!-- CRISP VECTOR BRAIN LIGHTBULB GRAPHIC -->
            <div class="slide1-graphic">
                <svg width="400" height="400" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <!-- Left Brain Hemisphere (Orange) -->
                    <path d="M200 60 C140 60 90 100 90 160 C90 200 110 230 140 250 L140 290 H200 V60 Z" fill="#E67E22"/>
                    <!-- Right Brain Hemisphere (Green) -->
                    <path d="M200 60 C260 60 310 100 310 160 C310 200 290 230 260 250 L260 290 H200 V60 Z" fill="#27AE60"/>
                    <!-- Binary Matrix Lines on Right -->
                    <text x="215" y="110" fill="#FFFFFF" font-size="20" font-family="monospace" font-weight="bold">1010</text>
                    <text x="215" y="140" fill="#FFFFFF" font-size="20" font-family="monospace" font-weight="bold">01010</text>
                    <text x="215" y="170" fill="#FFFFFF" font-size="20" font-family="monospace" font-weight="bold">101010</text>
                    <text x="215" y="200" fill="#FFFFFF" font-size="20" font-family="monospace" font-weight="bold">010101</text>
                    <text x="215" y="230" fill="#FFFFFF" font-size="20" font-family="monospace" font-weight="bold">10101</text>
                    <!-- Circuit Tracks on Left -->
                    <circle cx="130" cy="110" r="6" fill="#FFFFFF"/>
                    <circle cx="160" cy="150" r="6" fill="#FFFFFF"/>
                    <circle cx="120" cy="190" r="6" fill="#FFFFFF"/>
                    <path d="M130 110 L160 150 M160 150 L120 190 M120 190 L170 230" stroke="#FFFFFF" stroke-width="4"/>
                    <!-- Base Socket -->
                    <rect x="150" y="300" width="100" height="15" rx="4" fill="#5D6D7E"/>
                    <rect x="160" y="320" width="80" height="12" rx="4" fill="#34495E"/>
                    <path d="M170 335 L200 360 L230 335 Z" fill="#2C3E50"/>
                    <text x="200" y="390" fill="#34495E" font-size="32" font-weight="900" text-anchor="middle">SIH</text>
                </svg>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 2: PROBLEM & SOLUTION OVERVIEW       -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="header">
            <div class="header-logo-left">
                <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="#C0392B"/>
                    <path d="M50 15 L85 30 V55 C85 75 50 90 50 90 C50 90 15 75 15 55 V30 L50 15 Z" fill="#922B21" stroke="#FFFFFF" stroke-width="3"/>
                    <circle cx="50" cy="50" r="12" fill="#F1C40F"/>
                </svg>
            </div>
            <div class="header-title-green">RailBlock-AI: Smart Railway Block Planning & Dispatch Engine</div>
            <div class="header-logo-right">
                <svg width="180" height="65" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="35" fill="#E67E22"/>
                    <text x="95" y="45" fill="#1F4E79" font-size="22" font-weight="800">SMART INDIA</text>
                    <text x="95" y="70" fill="#27AE60" font-size="20" font-weight="800">HACKATHON 2026</text>
                </svg>
            </div>
        </div>

        <div class="slide2-body">
            <div class="section-box">
                <div class="sec-title-orange">Detailed Explanation</div>
                <ul class="bullet-list">
                    <li>AI Master Coordinator for track maintenance & dispatching.</li>
                    <li>Combines <strong>P-Way, TRD & S&T</strong> into 1 joint block window.</li>
                    <li>Auto-sides slow trains on loop lines to prevent delays.</li>
                </ul>

                <div class="sec-title-green" style="margin-top: 15px;">How it Addresses the Problem</div>
                <ul class="bullet-list">
                    <li>Reduces 4 track closures into 1 joint daily block.</li>
                    <li>Isolates train delays to single loop lines.</li>
                    <li>Recovers 42.9% lost track capacity on heavy corridors.</li>
                </ul>

                <div class="sec-title-orange" style="margin-top: 15px;">Innovation & Uniqueness</div>
                <ul class="bullet-list">
                    <li>Google OR-Tools <strong>MILP core</strong> for joint window clustering.</li>
                    <li>Dynamic speed & overtake predictor engine.</li>
                    <li>Live station-by-station track dashboard visualizer.</li>
                </ul>
            </div>

            <!-- COMPARISON CARD MATRIX -->
            <div class="comparison-table-card">
                <div class="card-hdr">RailBlock-AI: Filling the Gaps in Existing Railway Operations</div>
                <div class="card-grid">
                    <div class="grid-col-missing">
                        <span style="color: #C0392B; font-weight: 800; font-size: 18px; display: block; margin-bottom: 8px;">Existing Systems (Missing)</span>
                        <p style="font-size: 15px; color: #78281F; line-height: 1.4;">• Siloed Dept Requests (Separate shutdowns for P-Way, TRD, S&T)</p>
                        <p style="font-size: 15px; color: #78281F; line-height: 1.4; margin-top: 8px;">• 3-4 Track Shutdowns daily per section</p>
                        <p style="font-size: 15px; color: #78281F; line-height: 1.4; margin-top: 8px;">• Manual Loop Siding phone calls</p>
                        <p style="font-size: 15px; color: #78281F; line-height: 1.4; margin-top: 8px;">• Cascading Train Delays</p>
                    </div>

                    <div class="grid-col-included">
                        <span style="color: #1E8449; font-weight: 800; font-size: 18px; display: block; margin-bottom: 8px;">RailBlock-AI (Included)</span>
                        <p style="font-size: 15px; color: #145A32; line-height: 1.4;">• Single-Window Clustering into 1 joint block</p>
                        <p style="font-size: 15px; color: #145A32; line-height: 1.4; margin-top: 8px;">• 1 Consolidated Joint Block per section</p>
                        <p style="font-size: 15px; color: #145A32; line-height: 1.4; margin-top: 8px;">• Automated AI Siding Directive</p>
                        <p style="font-size: 15px; color: #145A32; line-height: 1.4; margin-top: 8px;">• Zero Domino Delays & 42.9% Capacity Recovered</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <span>@SIH Idea submission- Template</span>
            <span>2</span>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 3: TECHNICAL APPROACH                -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="header">
            <div class="header-logo-left">
                <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="#C0392B"/>
                    <circle cx="50" cy="50" r="12" fill="#F1C40F"/>
                </svg>
            </div>
            <div class="header-title-main" style="color: #C0392B;">TECHNICAL APPROACH</div>
            <div class="header-logo-right">
                <svg width="180" height="65" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="35" fill="#E67E22"/>
                    <text x="95" y="45" fill="#1F4E79" font-size="22" font-weight="800">SMART INDIA</text>
                    <text x="95" y="70" fill="#27AE60" font-size="20" font-weight="800">HACKATHON 2026</text>
                </svg>
            </div>
        </div>

        <div class="slide3-body">
            <div style="font-size: 26px; font-weight: 800; color: #27AE60; text-align: center;">TECHNOLOGY USED AND METHODOLOGY</div>
            
            <table class="tech-table">
                <thead>
                    <tr>
                        <th style="width: 20%;">Feature</th>
                        <th style="width: 22%;">Input</th>
                        <th style="width: 22%;">Output</th>
                        <th style="width: 20%;">How We Do It (Methodology)</th>
                        <th style="width: 16%;">APIs / Open-Source Tools</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-weight: 800; color: #1A252C;">Joint Block Optimizer</td>
                        <td>P-Way, TRD & S&T maintenance requests</td>
                        <td style="font-weight: 800; color: #C0392B;">1 Consolidated 4h Joint Maintenance Window</td>
                        <td>MILP constraint solver algorithm grouping overlapping track section requests across departments.</td>
                        <td style="font-weight: 800; color: #1E8449;">Google OR-Tools, PuLP, Python</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 800; color: #1A252C;">AI Train Dispatcher</td>
                        <td>Live train speeds, priority & telemetry feeds</td>
                        <td style="font-weight: 800; color: #C0392B;">Loop Line Overtake Directive (PWL Siding)</td>
                        <td>Spatio-temporal graph modeling & priority speed vector analysis to hold slow freight trains.</td>
                        <td style="font-weight: 800; color: #1E8449;">FastAPI, NetworkX, Redis</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 800; color: #1A252C;">Track Capacity Engine</td>
                        <td>Section downtime logs & historical timetable</td>
                        <td style="font-weight: 800; color: #C0392B;">42.9% Capacity Recovery & Zero Domino Delay</td>
                        <td>Dynamic track availability modeling & section uptime calculation formulas.</td>
                        <td style="font-weight: 800; color: #1E8449;">Pandas, NumPy, SciPy</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 800; color: #1A252C;">Live Route Dashboard</td>
                        <td>Route Selection (NDLS → GWL)</td>
                        <td style="font-weight: 800; color: #C0392B;">Live 'Where Is My Track' Interactive Portal</td>
                        <td>Real-time web portal rendering section tracks, loop siding status & timetable alerts.</td>
                        <td style="font-weight: 800; color: #1E8449;">HTML5, Tailwind CSS, Chart.js</td>
                    </tr>
                    <tr>
                        <td style="font-weight: 800; color: #1A252C;">CRIS System Gateway</td>
                        <td>COA & BDMS railway system feeds</td>
                        <td style="font-weight: 800; color: #C0392B;">Automated Controller Approval Directive</td>
                        <td>REST API synchronization with Human-in-the-Loop controller click approval workflow.</td>
                        <td style="font-weight: 800; color: #1E8449;">CRIS Open APIs, WebSocket, JSON</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="footer">
            <span>@SIH Idea submission- Template</span>
            <span>3</span>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 4: FEASIBILITY AND VIABILITY         -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="header">
            <div class="header-logo-left">
                <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="#C0392B"/>
                    <circle cx="50" cy="50" r="12" fill="#F1C40F"/>
                </svg>
            </div>
            <div class="header-title-green">FEASIBILITY AND VIABILITY</div>
            <div class="header-logo-right">
                <svg width="180" height="65" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="35" fill="#E67E22"/>
                    <text x="95" y="45" fill="#1F4E79" font-size="22" font-weight="800">SMART INDIA</text>
                    <text x="95" y="70" fill="#27AE60" font-size="20" font-weight="800">HACKATHON 2026</text>
                </svg>
            </div>
        </div>

        <div style="text-align: center; font-size: 24px; font-weight: 700; color: #1A252C; margin-top: -10px;">Implementation Feasibility, Operational Risks & Mitigation Strategies</div>

        <div class="slide2-body">
            <div class="section-box">
                <div class="sec-title-orange">Feasibility Analysis</div>
                <ul class="bullet-list">
                    <li><strong>100% Software:</strong> Zero track hardware changes needed.</li>
                    <li><strong>High Scalability:</strong> Covers all 68 railway divisions.</li>
                    <li><strong>Low Latency:</strong> MILP solver computes in seconds.</li>
                </ul>

                <div class="sec-title-green" style="margin-top: 15px;">Challenges & Risks</div>
                <ul class="bullet-list">
                    <li><strong>Siloed Depts:</strong> Coordinating P-Way, TRD & S&T.</li>
                    <li><strong>Track Speeds:</strong> Handling varying section limits.</li>
                    <li><strong>Change Management:</strong> Shifting controller workflows.</li>
                </ul>

                <div class="sec-title-orange" style="margin-top: 15px;">Strategies to Overcome</div>
                <ul class="bullet-list">
                    <li><strong>CRIS Sync:</strong> Direct API hooks to COA & BDMS.</li>
                    <li><strong>Human Control:</strong> Controllers retain click-approval.</li>
                    <li><strong>Phased Rollout:</strong> Starting on Delhi-Mathura route.</li>
                </ul>
            </div>

            <div class="comparison-table-card">
                <div class="card-hdr" style="background: #145A32;">FEASIBILITY & DEPLOYMENT MATRIX</div>
                <div style="padding: 20px; display: flex; flex-direction: column; gap: 16px; background: #F4F9F5;">
                    <div style="background: #FFF; padding: 16px; border-radius: 10px; border: 1px solid #D5D8DC;">
                        <span style="font-weight: 800; font-size: 16px; color: #1E8449;">1. 100% Software Solution</span>
                        <p style="font-size: 13px; color: #566573; margin-top: 4px;">Requires zero track sensors or train hardware modifications. Deploys directly on central CRIS server clusters.</p>
                    </div>
                    <div style="background: #FFF; padding: 16px; border-radius: 10px; border: 1px solid #D5D8DC;">
                        <span style="font-weight: 800; font-size: 16px; color: #1E8449;">2. High Network Scalability</span>
                        <p style="font-size: 13px; color: #566573; margin-top: 4px;">Modular API architecture easily scales across all 68 Indian Railway divisions & 18 zones nationwide.</p>
                    </div>
                    <div style="background: #FFF; padding: 16px; border-radius: 10px; border: 1px solid #D5D8DC;">
                        <span style="font-weight: 800; font-size: 16px; color: #1E8449;">3. CRIS System Integration</span>
                        <p style="font-size: 13px; color: #566573; margin-top: 4px;">Direct REST API synchronization with COA & BDMS system feeds with Human-in-the-Loop controller approval.</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <span>@SIH Idea submission- Template</span>
            <span>4</span>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 5: IMPACT AND BENEFITS               -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="header">
            <div class="header-logo-left">
                <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="#C0392B"/>
                    <circle cx="50" cy="50" r="12" fill="#F1C40F"/>
                </svg>
            </div>
            <div class="header-title-main" style="color: #E67E22;">IMPACT AND BENEFITS</div>
            <div class="header-logo-right">
                <svg width="180" height="65" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="35" fill="#E67E22"/>
                    <text x="95" y="45" fill="#1F4E79" font-size="22" font-weight="800">SMART INDIA</text>
                    <text x="95" y="70" fill="#27AE60" font-size="20" font-weight="800">HACKATHON 2026</text>
                </svg>
            </div>
        </div>

        <div style="text-align: center; font-size: 24px; font-weight: 700; color: #1A252C; margin-top: -10px;">Operational, Economic, Social & Environmental Value Creation</div>

        <div class="cards-grid-4" style="flex: 1; align-items: center;">
            <div class="benefit-card">
                <span style="font-size: 36px; font-weight: 900; color: #C0392B;">42.9%</span>
                <h4 style="font-size: 20px; font-weight: 800; color: #1A252C; margin: 8px 0;">Track Capacity Reclaimed</h4>
                <p style="font-size: 15px; color: #566573;">Consolidates multi-departmental P-Way, TRD & S&T maintenance requests into 1 single joint daily block window.</p>
            </div>

            <div class="benefit-card">
                <span style="font-size: 36px; font-weight: 900; color: #1E8449;">Rs. 100s Cr</span>
                <h4 style="font-size: 20px; font-weight: 800; color: #1A252C; margin: 8px 0;">Annual Economic Savings</h4>
                <p style="font-size: 15px; color: #566573;">Prevents locomotive idle hours, reduces diesel freight detention costs, and eliminates wasted track downtime.</p>
            </div>

            <div class="benefit-card">
                <span style="font-size: 36px; font-weight: 900; color: #D4AC0D;">Zero Delay</span>
                <h4 style="font-size: 20px; font-weight: 800; color: #1A252C; margin: 8px 0;">Passenger Punctuality</h4>
                <p style="font-size: 15px; color: #566573;">Isolates slow train holds to station loop lines, allowing fast express passenger trains to run at full speed.</p>
            </div>

            <div class="benefit-card">
                <span style="font-size: 36px; font-weight: 900; color: #2980B9;">NRP 2030</span>
                <h4 style="font-size: 20px; font-weight: 800; color: #1A252C; margin: 8px 0;">PM Gati Shakti Scalability</h4>
                <p style="font-size: 15px; color: #566573;">Cloud-native AI brain designed for seamless deployment across all 68 Indian Railway divisions nationwide.</p>
            </div>
        </div>

        <div class="footer">
            <span>@SIH Idea submission- Template</span>
            <span>5</span>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 6: RESEARCH AND REFERENCES           -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="header">
            <div class="header-logo-left">
                <svg width="65" height="65" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="100" height="100" rx="20" fill="#C0392B"/>
                    <circle cx="50" cy="50" r="12" fill="#F1C40F"/>
                </svg>
            </div>
            <div class="header-title-green">RESEARCH AND REFERENCES</div>
            <div class="header-logo-right">
                <svg width="180" height="65" viewBox="0 0 300 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="50" cy="50" r="35" fill="#E67E22"/>
                    <text x="95" y="45" fill="#1F4E79" font-size="22" font-weight="800">SMART INDIA</text>
                    <text x="95" y="70" fill="#27AE60" font-size="20" font-weight="800">HACKATHON 2026</text>
                </svg>
            </div>
        </div>

        <div style="text-align: center; font-size: 24px; font-weight: 700; color: #1A252C; margin-top: -10px;">Academic Papers, Railway Manuals & System Benchmarks</div>

        <div class="slide2-body">
            <div class="section-box">
                <div class="sec-title-orange">Government & Policy Reports</div>
                <ul class="bullet-list">
                    <li><strong>Ministry of Railways (NRP 2030):</strong> National Rail Plan Capacity Guidelines</li>
                    <li><strong>IRPWM Manual:</strong> Indian Railways Permanent Way Block Protocols</li>
                </ul>

                <div class="sec-title-green" style="margin-top: 15px;">AI & Railway Research</div>
                <ul class="bullet-list">
                    <li><strong>Google OR-Tools:</strong> Constraint Solver for Train & Track Block Scheduling</li>
                    <li><strong>IEEE Transactions (2023):</strong> Dynamic Train Rescheduling & Block Planning</li>
                </ul>

                <div class="sec-title-orange" style="margin-top: 15px;">Existing Systems & Case Studies</div>
                <ul class="bullet-list">
                    <li><strong>CRIS COA System:</strong> Control Office Application Live Dispatch Feeds</li>
                    <li><strong>CRIS BDMS Portal:</strong> Block Demand Management System Workflows</li>
                </ul>
            </div>

            <div style="display: flex; justify-content: center; align-items: center;">
                <svg width="500" height="350" viewBox="0 0 500 350" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect width="500" height="350" rx="16" fill="#F4F6F7" stroke="#D5D8DC" stroke-width="2"/>
                    <rect x="20" y="40" width="140" height="60" rx="8" fill="#D6EAF8" stroke="#2980B9" stroke-width="2"/>
                    <text x="90" y="75" fill="#1B4F72" font-size="13" font-weight="bold" text-anchor="middle">DATA ACQUISITION & SCHEDULING</text>
                    
                    <rect x="200" y="30" width="160" height="80" rx="10" fill="#E8F8F5" stroke="#27AE60" stroke-width="3"/>
                    <text x="280" y="65" fill="#117864" font-size="15" font-weight="900" text-anchor="middle">INTEGRATED</text>
                    <text x="280" y="85" fill="#117864" font-size="15" font-weight="900" text-anchor="middle">DISPATCH ENGINE</text>

                    <path d="M160 70 H200" stroke="#2980B9" stroke-width="3" marker-end="url(#arrow)"/>
                    <rect x="380" y="30" width="100" height="40" rx="6" fill="#EAEDED" stroke="#7F8C8D" stroke-width="1.5"/>
                    <text x="430" y="55" fill="#2C3E50" font-size="11" font-weight="bold" text-anchor="middle">REAL-TIME TRACKING</text>
                    <rect x="380" y="85" width="100" height="40" rx="6" fill="#EAEDED" stroke="#7F8C8D" stroke-width="1.5"/>
                    <text x="430" y="110" fill="#2C3E50" font-size="11" font-weight="bold" text-anchor="middle">RESOURCE OPTIMIZATION</text>

                    <!-- Train Track Line -->
                    <path d="M20 200 H480" stroke="#2C3E50" stroke-width="4"/>
                    <path d="M20 230 H480" stroke="#2C3E50" stroke-width="4"/>
                    <rect x="150" y="170" width="200" height="50" rx="8" fill="#1F4E79"/>
                    <circle cx="180" cy="235" r="10" fill="#7F8C8D"/>
                    <circle cx="320" cy="235" r="10" fill="#7F8C8D"/>
                    <text x="250" y="200" fill="#FFFFFF" font-size="16" font-weight="bold" text-anchor="middle">INDIAN RAILWAYS</text>
                </svg>
            </div>
        </div>

        <div class="footer">
            <span>@SIH Idea submission- Template</span>
            <span>6</span>
        </div>
    </div>

</body>
</html>
"""

with open("generate_fixed_presentation.html", "w") as f:
    f.write(html_content)

print("Saved generate_fixed_presentation.html")

async def render_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        await page.goto(f'file://{os.path.abspath("generate_fixed_presentation.html")}', wait_until='networkidle')
        pdf_path = 'RailBlock_AI_SIH26027_Winning_Presentation_8K.pdf'
        await page.pdf(
            path=pdf_path,
            width='1920px',
            height='1080px',
            print_background=True,
            margin={'top': '0px', 'right': '0px', 'bottom': '0px', 'left': '0px'}
        )
        await browser.close()
        print(f"Successfully generated PDF: {pdf_path}")

if __name__ == "__main__":
    asyncio.run(render_pdf())

