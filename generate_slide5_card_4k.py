import os
import textwrap
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

font_header = ImageFont.truetype(font_bold_path, 68)
font_sub_header = ImageFont.truetype(font_bold_path, 48)
font_metric_num = ImageFont.truetype(font_bold_path, 84)
font_card_title = ImageFont.truetype(font_bold_path, 44)
font_regular = ImageFont.truetype(font_path, 34)

# Outer Frame
draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=32, fill="#FAFDFB", outline="#A5D6A7", width=6)

# Header Banner
header_height = 220
draw.rounded_rectangle([20, 20, width - 20, header_height], radius=32, fill="#1B5E20")

h_text = "IMPACT & BENEFITS MATRIX"
hb = font_header.getbbox(h_text)
hw = hb[2] - hb[0]
draw.text(((width - hw) // 2, 45), h_text, font=font_header, fill="#FFFFFF")

sh_text = "Quantifiable Value Delivered Across Indian Railways Network"
shb = font_sub_header.getbbox(sh_text)
shw = shb[2] - shb[0]
draw.text(((width - shw) // 2, 135), sh_text, font=font_sub_header, fill="#C8E6C9")

# Top 2 Metric Cards
# Card 1: 42.9% Capacity
draw.rounded_rectangle([60, 260, 1160, 720], radius=24, fill="#E8F5E9", outline="#A5D6A7", width=4)
draw.text((100, 300), "42.9%", font=font_metric_num, fill="#1B5E20")
draw.text((100, 420), "Track Capacity Reclaimed", font=font_card_title, fill="#0D2B45")

desc1 = "Consolidates multi-dept maintenance shutdowns into single joint windows."
d1_lines = textwrap.wrap(desc1, width=36)
dy = 490
for l in d1_lines:
    draw.text((100, dy), l, font=font_regular, fill="#37474F")
    dy += 50

# Card 2: Rs. 100s Cr Saved
draw.rounded_rectangle([1240, 260, 2340, 720], radius=24, fill="#FFEBEE", outline="#FFCDD2", width=4)
draw.text((1280, 300), "Rs. 100s Cr", font=font_metric_num, fill="#C8102E")
draw.text((1280, 420), "Annual Economic Savings", font=font_card_title, fill="#0D2B45")

desc2 = "Cuts locomotive idle time, freight detention & fuel wastage."
d2_lines = textwrap.wrap(desc2, width=36)
dy = 490
for l in d2_lines:
    draw.text((1280, dy), l, font=font_regular, fill="#37474F")
    dy += 50

# Bottom 3 Category Cards
categories = [
    {
        "x1": 60, "x2": 790,
        "bg": "#FFF3E0", "border": "#FFE0B2",
        "title": "Passenger Experience",
        "color": "#E65100",
        "desc": "Predictable, on-time train journeys with zero surprise domino delays."
    },
    {
        "x1": 835, "x2": 1565,
        "bg": "#E3F2FD", "border": "#BBDEFB",
        "title": "Environmental Impact",
        "color": "#0D47A1",
        "desc": "Reduces diesel idling carbon emissions & optimizes electric traction."
    },
    {
        "x1": 1610, "x2": 2340,
        "bg": "#F3E5F5", "border": "#E1BEE7",
        "title": "PM Gati Shakti Scale",
        "color": "#4A148C",
        "desc": "Scalable AI brain for National Rail Plan 2030 capacity expansion."
    }
]

for cat in categories:
    draw.rounded_rectangle([cat["x1"], 760, cat["x2"], 1900], radius=24, fill=cat["bg"], outline=cat["border"], width=4)
    draw.text((cat["x1"] + 40, 810), cat["title"], font=font_card_title, fill=cat["color"])
    
    desc_lines = textwrap.wrap(cat["desc"], width=24)
    dy = 920
    for l in desc_lines:
        draw.text((cat["x1"] + 40, dy), l, font=font_regular, fill="#37474F")
        dy += 54

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide5_impact_card_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide5_impact_card_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("4K Slide 5 Card generated successfully!")
