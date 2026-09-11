import os
import math
from PIL import Image, ImageDraw, ImageFont

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

# Portrait Aspect Ratio (4:5) to fit Canva Right Box perfectly
width = 1600
height = 2000

img = Image.new("RGB", (width, height), "#FFFFFF")
draw = ImageDraw.Draw(img)

font_header = ImageFont.truetype(font_bold_path, 54)
font_sub = ImageFont.truetype(font_bold_path, 38)
font_card_title = ImageFont.truetype(font_bold_path, 42)
font_bold = ImageFont.truetype(font_bold_path, 36)
font_regular = ImageFont.truetype(font_path, 32)

# Outer Card Frame (Soft Mint/Teal background like Canva template)
draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=36, fill="#E0F2F1", outline="#80CBC4", width=5)

# Inner White Paper/Board Background
draw.rounded_rectangle([60, 60, width - 60, height - 60], radius=28, fill="#FFFFFF", outline="#B2DFDB", width=4)

# Top Card Header
draw.rounded_rectangle([60, 60, width - 60, 220], radius=28, fill="#00796B")
hb = font_header.getbbox("RAILBLOCK-AI RESEARCH")
hw = hb[2] - hb[0]
draw.text(((width - hw) // 2, 95), "RAILBLOCK-AI RESEARCH", font=font_header, fill="#FFFFFF")

# --- DRAWING ELEMENT 1: Railway Track & Vande Bharat Train Vector ---
train_y = 260
draw.rounded_rectangle([100, train_y, width - 100, train_y + 420], radius=24, fill="#E8F5E9", outline="#A5D6A7", width=3)

# Track
track_line_y = train_y + 330
draw.line([140, track_line_y, width - 140, track_line_y], fill="#37474F", width=10)
draw.line([140, track_line_y + 24], fill="#37474F", width=10)
for tx in range(160, width - 160, 50):
    draw.line([tx, track_line_y - 8, tx, track_line_y + 32], fill="#78909C", width=6)

# Vande Bharat Train
train_x = 220
draw.rounded_rectangle([train_x, train_y + 110, train_x + 850, train_y + 300], radius=24, fill="#0D2B45")
draw.polygon([(train_x + 850, train_y + 110), (train_x + 1020, train_y + 230), (train_x + 850, train_y + 300)], fill="#0D2B45")
draw.rectangle([train_x, train_y + 210, train_x + 950, train_y + 240], fill="#C8102E")
for wx in range(train_x + 80, train_x + 760, 120):
    draw.rounded_rectangle([wx, train_y + 135, wx + 85, train_y + 195], radius=10, fill="#80DEEA")
draw.polygon([(train_x + 800, train_y + 135), (train_x + 950, train_y + 180), (train_x + 800, train_y + 200)], fill="#00ACC1")

# --- DRAWING ELEMENT 2: AI Researcher / Control Center Console ---
console_y = 720
draw.rounded_rectangle([100, console_y, width - 100, console_y + 560], radius=24, fill="#F4F6F8", outline="#CFD8DC", width=3)

# Console Screen Header
draw.rounded_rectangle([100, console_y, width - 100, console_y + 90], radius=24, fill="#0D2B45")
draw.text((140, console_y + 24), "🖥️ LIVE DISPATCH CONSOLE & GNN MODEL", font=font_sub, fill="#FFFFFF")

# Graph Nodes Inside Console Screen
net_cx = width // 2
net_cy = console_y + 320

nodes = [
    (net_cx - 400, net_cy - 100, "P-Way"),
    (net_cx - 150, net_cy - 160, "TRD"),
    (net_cx - 150, net_cy - 40, "S&T"),
    (net_cx + 150, net_cy - 100, "OR-Tools MILP"),
    (net_cx + 400, net_cy - 160, "Loop Siding"),
    (net_cx + 400, net_cy - 40, "CRIS Sync")
]

edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
for u, v in edges:
    draw.line([nodes[u][0], nodes[u][1], nodes[v][0], nodes[v][1]], fill="#00897B", width=6)

for nx, ny, label in nodes:
    draw.ellipse([nx - 28, ny - 28, nx + 28, ny + 28], fill="#004D40", outline="#80CBC4", width=3)
    draw.ellipse([nx - 12, ny - 12, nx + 12, ny + 12], fill="#80DFEA")
    tb = font_bold.getbbox(label)
    tw = tb[2] - tb[0]
    draw.text((nx - tw // 2, ny + 34), label, font=font_bold, fill="#0D2B45")

# --- DRAWING ELEMENT 3: Verification Checklist Badge Cards ---
checklist_y = 1320
draw.rounded_rectangle([100, checklist_y, width - 100, height - 100], radius=24, fill="#FAFDFB", outline="#A5D6A7", width=3)

items = [
    ("✔  Google OR-Tools MILP", "Combinatorial optimization core for block scheduling."),
    ("✔  IRPWM Manual Standards", "Indian Railways Permanent Way safety compliance."),
    ("✔  CRIS COA & BDMS APIs", "Real-time train telemetry & dispatch API gateways.")
]

iy = checklist_y + 40
for title, desc in items:
    draw.rounded_rectangle([140, iy, width - 140, iy + 140], radius=16, fill="#FFFFFF", outline="#E0E0E0", width=2)
    draw.text((180, iy + 25), title, font=font_card_title, fill="#1B5E20")
    draw.text((180, iy + 80), desc, font=font_regular, fill="#546E7A")
    iy += 170

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide6_canva_illustration_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide6_canva_illustration_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("4K Slide 6 Canva Illustration generated successfully!")
