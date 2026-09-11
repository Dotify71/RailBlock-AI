import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# Load crisp system font
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

# 4K Ultra High-Res Dimensions (4x scale)
width = 2400
height = 1960

img = Image.new("RGB", (width, height), "#FFFFFF")
draw = ImageDraw.Draw(img)

# Font sizes scaled for 4K
font_header = ImageFont.truetype(font_bold_path, 72)
font_sub_header = ImageFont.truetype(font_bold_path, 52)
font_col_title = ImageFont.truetype(font_bold_path, 56)
font_item_title = ImageFont.truetype(font_bold_path, 46)
font_item_desc = ImageFont.truetype(font_path, 40)
font_icon = ImageFont.truetype(font_bold_path, 52)

# Outer Card Frame
draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=32, fill="#FAFDFB", outline="#A5D6A7", width=6)

# Header Banner
header_height = 230
draw.rounded_rectangle([20, 20, width - 20, header_height], radius=32, fill="#1B5E20")

# Header Text
h_text = "RailBlock-AI: Filling the Gaps"
hb = font_header.getbbox(h_text)
hw = hb[2] - hb[0]
draw.text(((width - hw) // 2, 45), h_text, font=font_header, fill="#FFFFFF")

sh_text = "in Existing Railway Operations"
shb = font_sub_header.getbbox(sh_text)
shw = shb[2] - shb[0]
draw.text(((width - shw) // 2, 138), sh_text, font=font_sub_header, fill="#C8E6C9")

# Column Headers
col_y1 = 260
col_y2 = 380

col1_x1, col1_x2 = 60, 1160
col2_x1, col2_x2 = 1240, 2340

# Left Col Header (Red Missing)
draw.rounded_rectangle([col1_x1, col_y1, col1_x2, col_y2], radius=20, fill="#FFEBEE", outline="#FFCDD2", width=4)
t1 = "Existing Systems (Missing)"
tb1 = font_col_title.getbbox(t1)
tw1 = tb1[2] - tb1[0]
draw.text((col1_x1 + (1100 - tw1) // 2, col_y1 + 32), t1, font=font_col_title, fill="#C8102E")

# Right Col Header (Green Included)
draw.rounded_rectangle([col2_x1, col_y1, col2_x2, col_y2], radius=20, fill="#E8F5E9", outline="#C8E6C9", width=4)
t2 = "RailBlock-AI (Included)"
tb2 = font_col_title.getbbox(t2)
tw2 = tb2[2] - tb2[0]
draw.text((col2_x1 + (1100 - tw2) // 2, col_y1 + 32), t2, font=font_col_title, fill="#1B5E20")

# Rows Data
rows_data = [
    (
        "Siloed Dept Requests",
        "P-Way, TRD & S&T demand separate daily shutdowns.",
        "Single-Window AI Clustering",
        "Groups overlapping requests into 1 joint block."
    ),
    (
        "3-4 Track Shutdowns",
        "Multiple track closures per section every day.",
        "1 Consolidated Joint Block",
        "Combines track, overhead & signal work."
    ),
    (
        "Manual Loop Siding",
        "Phone calls & manual controller siding decisions.",
        "Automated AI Siding Directive",
        "Sides slow trains automatically on loop lines."
    ),
    (
        "Cascading Train Delays",
        "Domino delays propagate across trailing trains.",
        "Zero Domino Delays",
        "Fast express trains maintain full operational speed."
    ),
    (
        "Wasted Track Capacity",
        "40%+ track availability lost during maintenance.",
        "42.9% Capacity Recovered",
        "Maximizes section uptime & freight throughput."
    )
]

y_pos = 410
row_h = 280
spacing = 20

for title_off, desc_off, title_on, desc_on in rows_data:
    # Left Box (Existing)
    draw.rounded_rectangle([col1_x1, y_pos, col1_x2, y_pos + row_h], radius=16, fill="#FFFFFF", outline="#FFCDD2", width=3)
    
    # Red Cross Icon
    draw.text((col1_x1 + 30, y_pos + 30), "✖", font=font_icon, fill="#D32F2F")
    draw.text((col1_x1 + 100, y_pos + 32), title_off, font=font_item_title, fill="#C8102E")
    
    desc_off_lines = textwrap.wrap(desc_off, width=38)
    dy = y_pos + 110
    for l in desc_off_lines:
        draw.text((col1_x1 + 100, dy), l, font=font_item_desc, fill="#616161")
        dy += 54
        
    # Right Box (RailBlock-AI)
    draw.rounded_rectangle([col2_x1, y_pos, col2_x2, y_pos + row_h], radius=16, fill="#FFFFFF", outline="#C8E6C9", width=3)
    
    # Green Check Icon
    draw.text((col2_x1 + 30, y_pos + 30), "✔", font=font_icon, fill="#2E7D32")
    draw.text((col2_x1 + 100, y_pos + 32), title_on, font=font_item_title, fill="#1B5E20")
    
    desc_on_lines = textwrap.wrap(desc_on, width=38)
    dy = y_pos + 110
    for l in desc_on_lines:
        draw.text((col2_x1 + 100, dy), l, font=font_item_desc, fill="#37474F")
        dy += 54
        
    y_pos += row_h + spacing

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide2_comparison_card_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide2_comparison_card_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("4K Ultra High-Res Slide 2 Card generated successfully!")
