import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Find system font
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

font_header = ImageFont.truetype(font_bold_path, 22)
font_title = ImageFont.truetype(font_bold_path, 32)
font_bold = ImageFont.truetype(font_bold_path, 18)
font_regular = ImageFont.truetype(font_path, 17)

columns = [
    {"name": "Feature", "width": 220, "align": "center"},
    {"name": "Input", "width": 250, "align": "left"},
    {"name": "Output", "width": 260, "align": "left"},
    {"name": "How We Do It (Methodology)", "width": 450, "align": "left"},
    {"name": "APIs / Open-Source Tools", "width": 260, "align": "left"}
]

rows = [
    [
        "Joint Block\nOptimizer",
        "P-Way, TRD & S&T maintenance requests",
        "1 Consolidated 4h Joint Maintenance Window",
        "MILP constraint solver algorithm grouping overlapping track section requests across departments.",
        "Google OR-Tools, PuLP, Python"
    ],
    [
        "AI Train\nDispatcher",
        "Live train speeds, priority & telemetry feeds",
        "Loop Line Overtake Directive (PWL Siding)",
        "Spatio-temporal graph modeling & priority speed vector analysis to hold slow freight trains.",
        "FastAPI, NetworkX, Redis"
    ],
    [
        "Track Capacity\nEngine",
        "Section downtime logs & historical timetable",
        "42.9% Capacity Recovery & Zero Domino Delay",
        "Dynamic track availability modeling & section uptime calculation formulas.",
        "Pandas, NumPy, SciPy"
    ],
    [
        "Live Route\nDashboard",
        "Route Selection (NDLS → GWL)",
        "Live 'Where Is My Track' Interactive Portal",
        "Real-time web portal rendering section tracks, loop siding status & timetable alerts.",
        "HTML5, Tailwind CSS, Chart.js"
    ],
    [
        "CRIS System\nGateway",
        "COA & BDMS railway system feeds",
        "Automated Controller Approval Directive",
        "REST API synchronization with Human-in-the-Loop controller click approval workflow.",
        "CRIS Open APIs, WebSocket, JSON"
    ]
]

padding_x = 16
padding_y = 18
header_height = 56
margin_top = 80
margin_left = 30
margin_bottom = 30

# Calculate heights per row
row_heights = []
for row_idx, row in enumerate(rows):
    max_lines = 1
    for col_idx, text in enumerate(row):
        col_w = columns[col_idx]["width"] - 2 * padding_x
        # Word wrap text
        lines = []
        for line in text.split('\n'):
            wrapped = textwrap.wrap(line, width=int(col_w / 9.5))
            lines.extend(wrapped if wrapped else [''])
        if len(lines) > max_lines:
            max_lines = len(lines)
    row_heights.append(max_lines * 24 + 2 * padding_y)

total_width = margin_left * 2 + sum(col["width"] for col in columns)
total_height = margin_top + header_height + sum(row_heights) + margin_bottom

img = Image.new("RGB", (total_width, total_height), "#FFFFFF")
draw = ImageDraw.Draw(img)

# Draw Title
title_text = "TECHNOLOGY USED AND METHODOLOGY"
title_bbox = font_title.getbbox(title_text)
title_w = title_bbox[2] - title_bbox[0]
draw.text(((total_width - title_w) // 2, 25), title_text, font=font_title, fill="#1B5E20")

# Draw Header Row
x_offset = margin_left
y_offset = margin_top

for col_idx, col in enumerate(columns):
    w = col["width"]
    draw.rectangle([x_offset, y_offset, x_offset + w, y_offset + header_height], fill="#E8F5E9", outline="#A5D6A7", width=2)
    
    bbox = font_header.getbbox(col["name"])
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    if col["align"] == "center":
        tx = x_offset + (w - tw) // 2
    else:
        tx = x_offset + padding_x
    ty = y_offset + (header_height - th) // 2 - 2
    draw.text((tx, ty), col["name"], font=font_header, fill="#0D2B45")
    x_offset += w

y_offset += header_height

# Draw Data Rows
for row_idx, row in enumerate(rows):
    rh = row_heights[row_idx]
    bg_color = "#FFFFFF" if row_idx % 2 == 0 else "#F7FAF7"
    x_offset = margin_left
    
    for col_idx, text in enumerate(row):
        w = columns[col_idx]["width"]
        draw.rectangle([x_offset, y_offset, x_offset + w, y_offset + rh], fill=bg_color, outline="#CFD8DC", width=1)
        
        col_w = w - 2 * padding_x
        lines = []
        for line in text.split('\n'):
            wrapped = textwrap.wrap(line, width=int(col_w / 9.5))
            lines.extend(wrapped if wrapped else [''])
            
        f = font_bold if col_idx in (0, 2, 4) else font_regular
        color = "#0D2B45" if col_idx == 0 else ("#C8102E" if col_idx == 2 else ("#1B5E20" if col_idx == 4 else "#212121"))
        
        line_y = y_offset + padding_y
        for l in lines:
            if columns[col_idx]["align"] == "center":
                lb = f.getbbox(l)
                lw = lb[2] - lb[0]
                lx = x_offset + (w - lw) // 2
            else:
                lx = x_offset + padding_x
            draw.text((lx, line_y), l, font=f, fill=color)
            line_y += 24
            
        x_offset += w
    y_offset += rh

output_file = "slide3_railblock_table.png"
img.save(output_file, "PNG", dpi=(300, 300))
print("High-res PNG table generated:", output_file)
