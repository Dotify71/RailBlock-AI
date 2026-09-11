import os
import math
from PIL import Image, ImageDraw, ImageFont

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

width = 2400
height = 1960

img = Image.new("RGB", (width, height), "#FFFFFF")
draw = ImageDraw.Draw(img)

font_title = ImageFont.truetype(font_bold_path, 64)
font_subtitle = ImageFont.truetype(font_path, 42)
font_card_title = ImageFont.truetype(font_bold_path, 48)
font_bold = ImageFont.truetype(font_bold_path, 38)
font_regular = ImageFont.truetype(font_path, 34)

# Outer Border Card Frame
draw.rounded_rectangle([30, 30, width - 30, height - 30], radius=36, fill="#F7FAFC", outline="#CFD8DC", width=6)

# --- 1. Top Section: Header Badge Illustration ---
draw.rounded_rectangle([100, 80, width - 100, 240], radius=24, fill="#0D2B45")
draw.text((160, 120), "RAILBLOCK-AI RESEARCH ENGINE", font=font_title, fill="#FFFFFF")
draw.text((width - 640, 132), "SIH 2026 ARCHITECTURE", font=font_subtitle, fill="#00E676")

# --- 2. Left Document Graphic Card ---
doc_x1, doc_y1, doc_x2, doc_y2 = 120, 300, 1140, 1850
draw.rounded_rectangle([doc_x1, doc_y1, doc_x2, doc_y2], radius=28, fill="#FFFFFF", outline="#B0BEC5", width=5)

draw.rounded_rectangle([doc_x1, doc_y1, doc_x2, doc_y1 + 140], radius=28, fill="#C8102E")
draw.text((doc_x1 + 60, doc_y1 + 45), "RESEARCH VERIFICATION", font=font_card_title, fill="#FFFFFF")

check_items = [
    ("Google OR-Tools MILP", "Constraint solver core for joint block window optimization."),
    ("IRPWM Manual Compliance", "Indian Railways Permanent Way safety & duration standards."),
    ("CRIS COA & BDMS Feeds", "Real-time train position tracking & dispatch API gateways."),
    ("Spatio-Temporal GNNs", "Graph neural networks for station bottleneck prediction.")
]

cy = doc_y1 + 200
for title, desc in check_items:
    draw.rounded_rectangle([doc_x1 + 40, cy, doc_x2 - 40, cy + 300], radius=20, fill="#F4F6F8", outline="#E0E0E0", width=3)
    draw.ellipse([doc_x1 + 70, cy + 35, doc_x1 + 130, cy + 95], fill="#2E7D32")
    draw.text((doc_x1 + 84, cy + 40), "✔", font=font_bold, fill="#FFFFFF")
    
    draw.text((doc_x1 + 160, cy + 40), title, font=font_bold, fill="#0D2B45")
    
    words = desc.split(' ')
    l1 = " ".join(words[:5])
    l2 = " ".join(words[5:])
    draw.text((doc_x1 + 160, cy + 110), l1, font=font_regular, fill="#546E7A")
    if l2:
        draw.text((doc_x1 + 160, cy + 170), l2, font=font_regular, fill="#546E7A")
        
    cy += 340

# --- 3. Right Drawing Element: Train & Graph Illustration ---
right_x1, right_y1, right_x2, right_y2 = 1220, 300, 2280, 1850
draw.rounded_rectangle([right_x1, right_y1, right_x2, right_y2], radius=28, fill="#FFFFFF", outline="#B0BEC5", width=5)

draw.rounded_rectangle([right_x1, right_y1, right_x2, right_y1 + 140], radius=28, fill="#1565C0")
draw.text((right_x1 + 60, right_y1 + 45), "AI DISPATCH GRAPH MODEL", font=font_card_title, fill="#FFFFFF")

# Train Illustration Box
train_box_y = right_y1 + 200
draw.rounded_rectangle([right_x1 + 60, train_box_y, right_x2 - 60, train_box_y + 450], radius=24, fill="#E3F2FD", outline="#90CAF9", width=3)

track_y = train_box_y + 360
draw.line([right_x1 + 100, track_y, right_x2 - 100, track_y], fill="#37474F", width=12)
draw.line([right_x1 + 100, track_y + 30, right_x2 - 100, track_y + 30], fill="#37474F", width=12)
for tx in range(right_x1 + 120, right_x2 - 120, 60):
    draw.line([tx, track_y - 10, tx, track_y + 40], fill="#78909C", width=8)

train_x = right_x1 + 180
draw.rounded_rectangle([train_x, train_box_y + 120, train_x + 600, train_box_y + 330], radius=30, fill="#0D2B45")
draw.polygon([(train_x + 600, train_box_y + 120), (train_x + 740, train_box_y + 260), (train_x + 600, train_box_y + 330)], fill="#0D2B45")
draw.rectangle([train_x, train_box_y + 230, train_x + 700, train_box_y + 260], fill="#C8102E")
for wx in range(train_x + 60, train_x + 520, 110):
    draw.rounded_rectangle([wx, train_box_y + 150, wx + 80, train_box_y + 210], radius=10, fill="#80DEEA")
draw.polygon([(train_x + 560, train_box_y + 150), (train_x + 670, train_box_y + 200), (train_x + 560, train_box_y + 220)], fill="#00ACC1")

# Graph Drawing Box
net_y = train_box_y + 520
draw.rounded_rectangle([right_x1 + 60, net_y, right_x2 - 60, right_y2 - 50], radius=24, fill="#FFF8E1", outline="#FFE082", width=3)

nodes = [
    (right_x1 + 180, net_y + 140, "P-Way"),
    (right_x1 + 430, net_y + 70, "TRD"),
    (right_x1 + 430, net_y + 210, "S&T"),
    (right_x1 + 680, net_y + 140, "MILP Core"),
    (right_x1 + 860, net_y + 70, "PWL Siding"),
    (right_x1 + 860, net_y + 210, "COA Sync")
]

edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5)]
for u, v in edges:
    draw.line([nodes[u][0], nodes[u][1], nodes[v][0], nodes[v][1]], fill="#FFB300", width=8)

for nx, ny, label in nodes:
    draw.ellipse([nx - 32, ny - 32, nx + 32, ny + 32], fill="#0D2B45", outline="#FF6F00", width=4)
    draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], fill="#FFD54F")
    
    # Calculate label width to center it
    tb = font_bold.getbbox(label)
    tw = tb[2] - tb[0]
    draw.text((nx - tw // 2, ny + 40), label, font=font_bold, fill="#0D2B45")

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide6_drawing_illustration_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide6_drawing_illustration_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("4K Slide 6 Drawing Illustration generated successfully!")
