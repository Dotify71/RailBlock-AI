"""
RailBlock-AI Vector Asset Generator
Generates clean, scalable SVG vector brand assets according to SIH 2026 guidelines.
"""

import os

OUTPUT_DIR = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/frontend/assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Colors
RED = "#C8102E"
NAVY = "#0D2B45"
WHITE = "#FFFFFF"

# 1. Standalone App Icon (Square with rounded corners)
SVG_APP_ICON = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="112" fill="{RED}"/>
  <g transform="translate(0, 0)">
    <!-- Unified Shield Contour -->
    <path d="M256 70 C340 70 410 100 410 180 C410 320 256 430 256 430 C256 430 102 320 102 180 C102 100 172 70 256 70 Z" fill="none" stroke="{WHITE}" stroke-width="28" stroke-linejoin="round"/>
    
    <!-- Railway Tracks forming the core of shield -->
    <!-- Left Rail -->
    <path d="M185 150 L205 350" stroke="{WHITE}" stroke-width="20" stroke-linecap="round"/>
    <!-- Right Rail -->
    <path d="M327 150 L307 350" stroke="{WHITE}" stroke-width="20" stroke-linecap="round"/>
    
    <!-- Sleepers (Track Crossbars) -->
    <line x1="192" y1="200" x2="320" y2="200" stroke="{WHITE}" stroke-width="16" stroke-linecap="round"/>
    <line x1="197" y1="250" x2="315" y2="250" stroke="{WHITE}" stroke-width="16" stroke-linecap="round"/>
    <line x1="201" y1="300" x2="311" y2="300" stroke="{WHITE}" stroke-width="16" stroke-linecap="round"/>

    <!-- Subtle AI Integrated Nodes on Tracks -->
    <circle cx="197" cy="250" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <circle cx="315" cy="250" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <circle cx="256" cy="300" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    
    <!-- Subtle Connecting AI Vector Line -->
    <path d="M197 250 L256 300 L315 250" fill="none" stroke="{NAVY}" stroke-width="8"/>
  </g>
</svg>'''

# 2. Horizontal Logo on Light Background
SVG_HORIZONTAL_LIGHT = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" width="900" height="260">
  <!-- Symbol -->
  <g transform="translate(20, 20) scale(0.43)">
    <path d="M256 70 C340 70 410 100 410 180 C410 320 256 430 256 430 C256 430 102 320 102 180 C102 100 172 70 256 70 Z" fill="{RED}"/>
    <path d="M185 150 L205 350" stroke="{WHITE}" stroke-width="22" stroke-linecap="round"/>
    <path d="M327 150 L307 350" stroke="{WHITE}" stroke-width="22" stroke-linecap="round"/>
    <line x1="192" y1="200" x2="320" y2="200" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>
    <line x1="197" y1="250" x2="315" y2="250" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>
    <line x1="201" y1="300" x2="311" y2="300" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>
    <circle cx="197" cy="250" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <circle cx="315" cy="250" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <circle cx="256" cy="300" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <path d="M197 250 L256 300 L315 250" fill="none" stroke="{NAVY}" stroke-width="8"/>
  </g>
  
  <!-- Wordmark -->
  <text x="240" y="160" font-family="Public Sans, Inter, system-ui, sans-serif" font-weight="900" font-size="82" letter-spacing="-1">
    <tspan fill="{NAVY}">RailBlock</tspan><tspan fill="{RED}">-AI</tspan>
  </text>
</svg>'''

# 3. Horizontal Logo on Dark Background
SVG_HORIZONTAL_DARK = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 260" width="900" height="260">
  <rect width="900" height="260" rx="16" fill="{NAVY}"/>
  <!-- Symbol -->
  <g transform="translate(20, 20) scale(0.43)">
    <path d="M256 70 C340 70 410 100 410 180 C410 320 256 430 256 430 C256 430 102 320 102 180 C102 100 172 70 256 70 Z" fill="{RED}"/>
    <path d="M185 150 L205 350" stroke="{WHITE}" stroke-width="22" stroke-linecap="round"/>
    <path d="M327 150 L307 350" stroke="{WHITE}" stroke-width="22" stroke-linecap="round"/>
    <line x1="192" y1="200" x2="320" y2="200" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>
    <line x1="197" y1="250" x2="315" y2="250" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>
    <line x1="201" y1="300" x2="311" y2="300" stroke="{WHITE}" stroke-width="18" stroke-linecap="round"/>
    <circle cx="197" cy="250" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <circle cx="315" cy="250" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <circle cx="256" cy="300" r="14" fill="{NAVY}" stroke="{WHITE}" stroke-width="6"/>
    <path d="M197 250 L256 300 L315 250" fill="none" stroke="{NAVY}" stroke-width="8"/>
  </g>
  
  <!-- Wordmark -->
  <text x="240" y="160" font-family="Public Sans, Inter, system-ui, sans-serif" font-weight="900" font-size="82" letter-spacing="-1">
    <tspan fill="{WHITE}">RailBlock</tspan><tspan fill="{RED}">-AI</tspan>
  </text>
</svg>'''

# Save vector SVG files
with open(os.path.join(OUTPUT_DIR, "railblock_ai_app_icon.svg"), "w") as f:
    f.write(SVG_APP_ICON)

with open(os.path.join(OUTPUT_DIR, "railblock_ai_logo_horizontal.svg"), "w") as f:
    f.write(SVG_HORIZONTAL_LIGHT)

with open(os.path.join(OUTPUT_DIR, "railblock_ai_logo_dark.svg"), "w") as f:
    f.write(SVG_HORIZONTAL_DARK)

print("✅ Generated vector SVG assets successfully!")
