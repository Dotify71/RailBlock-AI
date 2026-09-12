import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions for 8K resolution
WIDTH = 7680
HEIGHT = 4320

img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

# Fonts setup
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
font_reg_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

if not os.path.exists(font_bold_path):
    font_bold_path = "/System/Library/Fonts/Helvetica.ttc"
    font_reg_path = font_bold_path

# 8K Scaled font sizes
font_header = ImageFont.truetype(font_bold_path, 68)
font_cell_bold = ImageFont.truetype(font_bold_path, 58)
font_cell_reg = ImageFont.truetype(font_reg_path, 56)

# Column definitions (Total width = 7000 px)
columns = [
    {"name": "Feature", "width": 1150, "align": "left"},
    {"name": "Input", "width": 1350, "align": "left"},
    {"name": "Output", "width": 1450, "align": "left"},
    {"name": "How We Do It\n(Methodology)", "width": 1700, "align": "left"},
    {"name": "APIs / Open-Source Tools", "width": 1350, "align": "left"}
]

rows = [
    [
        "Joint Block Optimizer",
        "P-Way, TRD & S&T maintenance requests",
        "1 Consolidated 4h Joint Maintenance Window",
        "MILP constraint solver algorithm grouping overlapping track section requests across departments.",
        "Google OR-Tools, PuLP, Python"
    ],
    [
        "AI Train Dispatcher",
        "Live train speeds, priority & telemetry feeds",
        "Loop Line Overtake Directive (PWL Siding)",
        "Spatio-temporal graph modeling & priority speed vector analysis to hold slow freight trains.",
        "FastAPI, NetworkX, Redis"
    ],
    [
        "Track Capacity Engine",
        "Section downtime logs & historical timetable",
        "42.9% Capacity Recovery & Zero Domino Delay",
        "Dynamic track availability modeling & section uptime calculation formulas.",
        "Pandas, NumPy, SciPy"
    ],
    [
        "Live Route Dashboard",
        "Route Selection (NDLS → GWL)",
        "Live 'Where Is My Track' Interactive Portal",
        "Real-time web portal rendering section tracks, loop siding status & timetable alerts.",
        "HTML5, Tailwind CSS, Chart.js"
    ],
    [
        "CRIS System Gateway",
        "COA & BDMS railway system feeds",
        "Automated Controller Approval Directive",
        "REST API synchronization with Human-in-the-Loop controller click approval workflow.",
        "CRIS Open APIs, WebSocket, JSON"
    ]
]

padding_x = 45
padding_y = 50
header_height = 200
margin_left = 40
margin_top = 40

def wrap_text(text, width_px, font):
    lines = []
    for paragraph in text.split('\n'):
        words = paragraph.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] - bbox[0] <= width_px:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        if current_line:
            lines.append(' '.join(current_line))
    return lines

# Wrap cells & calculate row heights
row_data_wrapped = []
row_heights = []

for row in rows:
    cell_lines_list = []
    max_h = 0
    for col_idx, text in enumerate(row):
        col_w = columns[col_idx]["width"] - 2 * padding_x
        f = font_cell_bold if col_idx in (0, 2, 4) else font_cell_reg
        lines = wrap_text(text, col_w, f)
        cell_lines_list.append(lines)
        h = len(lines) * 75 + 2 * padding_y
        if h > max_h:
            max_h = h
    row_data_wrapped.append(cell_lines_list)
    row_heights.append(max_h)

# Draw Header Row
x_offset = margin_left
y_offset = margin_top

for col_idx, col in enumerate(columns):
    w = col["width"]
    # Light green background
    draw.rectangle([x_offset, y_offset, x_offset + w, y_offset + header_height], fill="#E8F5E9", outline="#A5D6A7", width=4)
    
    h_lines = col["name"].split('\n')
    total_h_text = len(h_lines) * 75
    start_y = y_offset + (header_height - total_h_text) // 2
    
    for hline in h_lines:
        bbox = font_header.getbbox(hline)
        tw = bbox[2] - bbox[0]
        if col["align"] == "center":
            tx = x_offset + (w - tw) // 2
        else:
            tx = x_offset + padding_x
        draw.text((tx, start_y), hline, font=font_header, fill="#1B5E20")
        start_y += 75
        
    x_offset += w

y_offset += header_height

# Draw Table Data Rows
for row_idx, cell_lines_list in enumerate(row_data_wrapped):
    rh = row_heights[row_idx]
    bg_color = "#FFFFFF" if row_idx % 2 == 0 else "#F9FDF9"
    x_offset = margin_left
    
    for col_idx, lines in enumerate(cell_lines_list):
        w = columns[col_idx]["width"]
        draw.rectangle([x_offset, y_offset, x_offset + w, y_offset + rh], fill=bg_color, outline="#C8E6C9", width=3)
        
        f = font_cell_bold if col_idx in (0, 2, 4) else font_cell_reg
        
        if col_idx == 0:
            color = "#0B2545"  # Navy Blue Feature
        elif col_idx == 2:
            color = "#C8102E"  # Railway Red Output
        elif col_idx == 4:
            color = "#1B5E20"  # Green Tech Stack
        else:
            color = "#212121"  # Regular dark text
            
        text_block_h = len(lines) * 75
        start_y = y_offset + (rh - text_block_h) // 2
        
        for l in lines:
            if columns[col_idx]["align"] == "center":
                lb = f.getbbox(l)
                lw = lb[2] - lb[0]
                lx = x_offset + (w - lw) // 2
            else:
                lx = x_offset + padding_x
            draw.text((lx, start_y), l, font=f, fill=color)
            start_y += 75
            
        x_offset += w
    y_offset += rh

# Crop image tightly around table only
table_total_width = sum(c["width"] for c in columns)
cropped_img = img.crop((margin_left, margin_top, margin_left + table_total_width, y_offset))

# Save Table-Only PNGs
out_workspace = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide3_table_only_8k.png"
out_artifacts = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide3_table_only_8k.png"

cropped_img.save(out_workspace, "PNG", dpi=(300, 300))
cropped_img.save(out_artifacts, "PNG", dpi=(300, 300))

print(f"✅ Table-Only 8K Image successfully saved to:\n1. {out_workspace}\n2. {out_artifacts}")
