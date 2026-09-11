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
font_card_title = ImageFont.truetype(font_bold_path, 48)
font_bold = ImageFont.truetype(font_bold_path, 42)
font_regular = ImageFont.truetype(font_path, 38)
font_tag = ImageFont.truetype(font_bold_path, 36)

# Outer Card Frame
draw.rounded_rectangle([20, 20, width - 20, height - 20], radius=32, fill="#FAFDFB", outline="#A5D6A7", width=6)

# Header Banner
header_height = 220
draw.rounded_rectangle([20, 20, width - 20, header_height], radius=32, fill="#1B5E20")

h_text = "FEASIBILITY & DEPLOYMENT MATRIX"
hb = font_header.getbbox(h_text)
hw = hb[2] - hb[0]
draw.text(((width - hw) // 2, 45), h_text, font=font_header, fill="#FFFFFF")

sh_text = "Indian Railways Enterprise Integration & Scalability Model"
shb = font_sub_header.getbbox(sh_text)
shw = shb[2] - shb[0]
draw.text(((width - shw) // 2, 135), sh_text, font=font_sub_header, fill="#C8E6C9")

# 4 Key Pillars Cards
pillars = [
    {
        "title": "1. 100% Software Solution",
        "tag": "ZERO CAPEX",
        "tag_bg": "#E8F5E9",
        "tag_color": "#1B5E20",
        "desc": "Requires zero track sensors or train hardware modifications. Deploys directly on central CRIS server clusters."
    },
    {
        "title": "2. High Network Scalability",
        "tag": "68 DIVISIONS",
        "tag_bg": "#E3F2FD",
        "tag_color": "#0D47A1",
        "desc": "Modular API architecture easily scales across all 68 Indian Railway divisions & 18 zones nationwide."
    },
    {
        "title": "3. CRIS System Integration",
        "tag": "LIVE API SYNC",
        "tag_bg": "#FFF3E0",
        "tag_color": "#E65100",
        "desc": "Direct REST API synchronization with COA & BDMS system feeds with Human-in-the-Loop controller approval."
    },
    {
        "title": "4. Phased Corridor Rollout",
        "tag": "DELHI-MATHURA",
        "tag_bg": "#FFEBEE",
        "tag_color": "#C8102E",
        "desc": "Initial pilot deployment on high-density Golden Quadrilateral trunk routes before pan-India expansion."
    }
]

y_pos = 260
card_h = 380

for p in pillars:
    draw.rounded_rectangle([60, y_pos, width - 60, y_pos + card_h], radius=24, fill="#FFFFFF", outline="#CFD8DC", width=4)
    
    # Title
    draw.text((100, y_pos + 40), "✔ " + p["title"], font=font_card_title, fill="#0D2B45")
    
    # Tag Badge
    tb = font_tag.getbbox(p["tag"])
    tw = tb[2] - tb[0]
    tag_x1 = width - 120 - tw - 40
    tag_x2 = width - 120
    draw.rounded_rectangle([tag_x1, y_pos + 35, tag_x2, y_pos + 105], radius=16, fill=p["tag_bg"])
    draw.text((tag_x1 + 20, y_pos + 48), p["tag"], font=font_tag, fill=p["tag_color"])
    
    # Description
    desc_lines = textwrap.wrap(p["desc"], width=72)
    dy = y_pos + 130
    for l in desc_lines:
        draw.text((100, dy), l, font=font_regular, fill="#424242")
        dy += 54
        
    y_pos += card_h + 30

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide4_feasibility_card_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide4_feasibility_card_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("4K Ultra High-Res Slide 4 Card generated successfully!")
