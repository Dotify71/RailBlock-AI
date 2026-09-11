import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

font_header = ImageFont.truetype(font_bold_path, 20)
font_col_title = ImageFont.truetype(font_bold_path, 15)
font_item_title = ImageFont.truetype(font_bold_path, 13)
font_item_desc = ImageFont.truetype(font_path, 12)

width = 640
height = 540

img = Image.new("RGB", (width, height), "#FFFFFF")
draw = ImageDraw.Draw(img)

# Card Container Background & Outer Border
draw.rectangle([0, 0, width, height], fill="#FAFDFB", outline="#C8E6C9", width=3)

# Header Banner (Green Theme like SIH Template)
draw.rectangle([0, 0, width, 65], fill="#1B5E20")

header_text = "RailBlock-AI: Filling the Gaps\nin Existing Railway Systems"
h_bbox = font_header.getbbox("RailBlock-AI: Filling the Gaps")
h_w = h_bbox[2] - h_bbox[0]
draw.text(((width - h_w) // 2, 10), "RailBlock-AI: Filling the Gaps", font=font_header, fill="#FFFFFF")
sub_h_text = "in Existing Railway Operations"
sh_bbox = font_col_title.getbbox(sub_h_text)
sh_w = sh_bbox[2] - sh_bbox[0]
draw.text(((width - sh_w) // 2, 38), sub_h_text, font=font_col_title, fill="#A5D6A7")

# Column Headers
# Left Col (Existing - Missing)
col1_x1, col1_x2 = 15, 310
draw.rectangle([col1_x1, 75, col1_x2, 108], fill="#FFEBEE")
draw.text((col1_x1 + 35, 84), "Existing Systems (Missing)", font=font_col_title, fill="#C8102E")

# Right Col (RailBlock-AI - Included)
col2_x1, col2_x2 = 325, 625
draw.rectangle([col2_x1, 75, col2_x2, 108], fill="#E8F5E9")
draw.text((col2_x1 + 35, 84), "RailBlock-AI (Included)", font=font_col_title, fill="#1B5E20")

# Comparison Rows
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

y_pos = 118
row_h = 80

for row_title_off, row_desc_off, row_title_on, row_desc_on in rows_data:
    # Left Box (Existing)
    draw.rectangle([col1_x1, y_pos, col1_x2, y_pos + row_h], fill="#FFFFFF", outline="#FFCDD2", width=1)
    draw.text((col1_x1 + 10, y_pos + 8), "✖  " + row_title_off, font=font_item_title, fill="#D32F2F")
    
    desc_off_lines = textwrap.wrap(row_desc_off, width=32)
    dy = y_pos + 30
    for l in desc_off_lines:
        draw.text((col1_x1 + 10, dy), l, font=font_item_desc, fill="#616161")
        dy += 16
        
    # Right Box (RailBlock-AI)
    draw.rectangle([col2_x1, y_pos, col2_x2, y_pos + row_h], fill="#FFFFFF", outline="#C8E6C9", width=1)
    draw.text((col2_x1 + 10, y_pos + 8), "✔  " + row_title_on, font=font_item_title, fill="#2E7D32")
    
    desc_on_lines = textwrap.wrap(row_desc_on, width=32)
    dy = y_pos + 30
    for l in desc_on_lines:
        draw.text((col2_x1 + 10, dy), l, font=font_item_desc, fill="#424242")
        dy += 16
        
    y_pos += row_h + 4

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide2_comparison_card.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide2_comparison_card.png"
img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("Slide 2 Comparison Card generated successfully!")
