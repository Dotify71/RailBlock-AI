import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Load fonts
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

font_main_title = ImageFont.truetype(font_bold_path, 34)
font_subtitle = ImageFont.truetype(font_bold_path, 22)
font_header = ImageFont.truetype(font_bold_path, 16)
font_bold = ImageFont.truetype(font_bold_path, 14)
font_regular = ImageFont.truetype(font_path, 14)

columns = [
    {"name": "Feature", "width": 190, "align": "center"},
    {"name": "Input", "width": 220, "align": "left"},
    {"name": "Output", "width": 240, "align": "left"},
    {"name": "How We Do It\n(Methodology)", "width": 380, "align": "left"},
    {"name": "APIs / Open-Source Tools", "width": 220, "align": "left"}
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

padding_x = 14
padding_y = 16
header_height = 54
margin_top = 110
margin_left = 40
margin_bottom = 40

def wrap_cell_text(text, width_px, font):
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

row_data_wrapped = []
row_heights = []

for row_idx, row in enumerate(rows):
    cell_lines_list = []
    max_h = 0
    for col_idx, text in enumerate(row):
        col_w = columns[col_idx]["width"] - 2 * padding_x
        f = font_bold if col_idx in (0, 2, 4) else font_regular
        lines = wrap_cell_text(text, col_w, f)
        cell_lines_list.append(lines)
        h = len(lines) * 20 + 2 * padding_y
        if h > max_h:
            max_h = h
    row_data_wrapped.append(cell_lines_list)
    row_heights.append(max_h)

table_width = sum(col["width"] for col in columns)
total_width = margin_left * 2 + table_width
total_height = margin_top + header_height + sum(row_heights) + margin_bottom

img = Image.new("RGB", (total_width, total_height), "#FFFFFF")
draw = ImageDraw.Draw(img)

# Main Title (Orange/Red like SIH template)
title1 = "TECHNICAL APPROACH"
t1_bbox = font_main_title.getbbox(title1)
t1_w = t1_bbox[2] - t1_bbox[0]
draw.text(((total_width - t1_w) // 2, 20), title1, font=font_main_title, fill="#D84315")

# Subtitle (Green like SIH template)
title2 = "TECHNOLOGY USED AND METHODOLOGY"
t2_bbox = font_subtitle.getbbox(title2)
t2_w = t2_bbox[2] - t2_bbox[0]
draw.text(((total_width - t2_w) // 2, 65), title2, font=font_subtitle, fill="#2E7D32")

# Draw Header Row
x_offset = margin_left
y_offset = margin_top

for col_idx, col in enumerate(columns):
    w = col["width"]
    draw.rectangle([x_offset, y_offset, x_offset + w, y_offset + header_height], fill="#F0F4F1", outline="#A5D6A7", width=2)
    
    h_lines = col["name"].split('\n')
    total_h_text = len(h_lines) * 18
    start_y = y_offset + (header_height - total_h_text) // 2
    
    for hline in h_lines:
        bbox = font_header.getbbox(hline)
        tw = bbox[2] - bbox[0]
        if col["align"] == "center":
            tx = x_offset + (w - tw) // 2
        else:
            tx = x_offset + padding_x
        draw.text((tx, start_y), hline, font=font_header, fill="#0D2B45")
        start_y += 18
        
    x_offset += w

y_offset += header_height

# Draw Table Rows
for row_idx, cell_lines_list in enumerate(row_data_wrapped):
    rh = row_heights[row_idx]
    bg_color = "#FFFFFF" if row_idx % 2 == 0 else "#F9FBF9"
    x_offset = margin_left
    
    for col_idx, lines in enumerate(cell_lines_list):
        w = columns[col_idx]["width"]
        draw.rectangle([x_offset, y_offset, x_offset + w, y_offset + rh], fill=bg_color, outline="#CFD8DC", width=1)
        
        f = font_bold if col_idx in (0, 2, 4) else font_regular
        
        if col_idx == 0:
            color = "#0D2B45"
        elif col_idx == 2:
            color = "#C8102E"  # Railway Red for Output
        elif col_idx == 4:
            color = "#1B5E20"  # Railway Green for Tech Stack
        else:
            color = "#212121"
            
        text_block_h = len(lines) * 20
        start_y = y_offset + (rh - text_block_h) // 2
        
        for l in lines:
            if columns[col_idx]["align"] == "center":
                lb = f.getbbox(l)
                lw = lb[2] - lb[0]
                lx = x_offset + (w - lw) // 2
            else:
                lx = x_offset + padding_x
            draw.text((lx, start_y), l, font=f, fill=color)
            start_y += 20
            
        x_offset += w
    y_offset += rh

output_path = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide3_perfect_table.png"
img.save(output_path, "PNG", dpi=(300, 300))
print("Perfect table image saved at:", output_path)
