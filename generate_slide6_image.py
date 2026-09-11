import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

font_main_title = ImageFont.truetype(font_bold_path, 34)
font_subtitle = ImageFont.truetype(font_bold_path, 18)
font_section_header = ImageFont.truetype(font_bold_path, 16)
font_bold = ImageFont.truetype(font_bold_path, 13.5)
font_regular = ImageFont.truetype(font_path, 13.5)
font_url = ImageFont.truetype(font_path, 12)

width = 1280
height = 720

img = Image.new("RGB", (width, height), "#FFFFFF")
draw = ImageDraw.Draw(img)

# Top Title
title_text = "RESEARCH AND REFERENCES"
t_bbox = font_main_title.getbbox(title_text)
t_w = t_bbox[2] - t_bbox[0]
draw.text(((width - t_w) // 2, 40), title_text, font=font_main_title, fill="#2E7D32")

# Subtitle
sub_text = "Academic Papers, Railway Manuals & System Benchmarks"
s_bbox = font_subtitle.getbbox(sub_text)
s_w = s_bbox[2] - s_bbox[0]
draw.text(((width - s_w) // 2, 85), sub_text, font=font_subtitle, fill="#0D2B45")

# Left Column Content
sections = [
    {
        "title": "Government & Policy Reports",
        "title_color": "#D84315",
        "items": [
            ("• Ministry of Railways (NRP 2030) – ", "National Rail Plan Guidelines"),
            ("👉 https://indianrailways.gov.in", "url"),
            ("• IRPWM Manual – ", "Indian Railways Permanent Way Block Protocols")
        ]
    },
    {
        "title": "AI & Railway Research",
        "title_color": "#1B5E20",
        "items": [
            ("• Google OR-Tools – ", "Constraint Solver for Block Scheduling"),
            ("👉 https://developers.google.com/optimization", "url"),
            ("• IEEE Transactions (2023) – ", "Dynamic Train Rescheduling Studies")
        ]
    },
    {
        "title": "Existing Platforms & Case Studies",
        "title_color": "#D84315",
        "items": [
            ("• CRIS COA System – ", "Control Office Application Live Dispatch Feeds"),
            ("• CRIS BDMS Portal – ", "Block Demand Management System Workflows")
        ]
    },
    {
        "title": "Technical References",
        "title_color": "#0D2B45",
        "items": [
            ("• Spatio-Temporal Graph Neural Networks – ", "Railway Bottleneck Models"),
            ("• Python NetworkX & PuLP – ", "Network Routing & MILP Optimization Core")
        ]
    }
]

x_left = 60
y_start = 140

for sec in sections:
    # Section Header with diamond icon
    draw.text((x_left, y_start), "◆ " + sec["title"], font=font_section_header, fill=sec["title_color"])
    y_start += 24
    
    for prefix, body in sec["items"]:
        if body == "url":
            draw.text((x_left + 16, y_start), prefix, font=font_url, fill="#1976D2")
            y_start += 20
        else:
            draw.text((x_left + 14, y_start), prefix, font=font_bold, fill="#212121")
            p_bbox = font_bold.getbbox(prefix)
            pw = p_bbox[2] - p_bbox[0]
            draw.text((x_left + 14 + pw, y_start), body, font=font_regular, fill="#424242")
            y_start += 22
            
    y_start += 12

# Right Side Graphic Card
card_x1, card_y1, card_x2, card_y2 = 720, 140, 1220, 620
draw.rectangle([card_x1, card_y1, card_x2, card_y2], fill="#F4F8F5", outline="#C8E6C9", width=2)

# Graphic Card Header
draw.rectangle([card_x1, card_y1, card_x2, card_y1 + 50], fill="#2E7D32")
card_title = "RAILBLOCK-AI RESEARCH MATRIX"
ct_bbox = font_section_header.getbbox(card_title)
ct_w = ct_bbox[2] - ct_bbox[0]
draw.text((card_x1 + (500 - ct_w) // 2, card_y1 + 14), card_title, font=font_section_header, fill="#FFFFFF")

# Graphic Items inside Right Card
items = [
    ("Google OR-Tools MILP", "Combinatorial optimization core grouping P-Way, TRD & S&T blocks."),
    ("IRPWM Block Rules", "Standard safety interlocks & minimum window duration compliance."),
    ("CRIS COA API Gateway", "Real-time train position tracking & automatic timetable updates."),
    ("Graph Neural Networks", "Spatio-temporal congestion prediction across loop line sidings.")
]

gy = card_y1 + 75
for title, desc in items:
    draw.rectangle([card_x1 + 20, gy, card_x2 - 20, gy + 105], fill="#FFFFFF", outline="#E0E0E0", width=1)
    draw.text((card_x1 + 35, gy + 12), "✔ " + title, font=font_bold, fill="#0D2B45")
    
    wrapped_desc = textwrap.wrap(desc, width=42)
    dy = gy + 38
    for dline in wrapped_desc:
        draw.text((card_x1 + 35, dy), dline, font=font_regular, fill="#616161")
        dy += 18
    gy += 120

# Bottom Bar
draw.rectangle([0, 680, width, height], fill="#0288D1")
draw.text((width // 2 - 80, 692), "SIH 2026 Submission Template | Slide 6", font=font_url, fill="#FFFFFF")

output_path_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide6_railblock_preview.png"
output_path_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide6_railblock_preview.png"
img.save(output_path_art, "PNG", dpi=(300, 300))
img.save(output_path_proj, "PNG", dpi=(300, 300))
print("Slide 6 RailBlock preview generated successfully!")
