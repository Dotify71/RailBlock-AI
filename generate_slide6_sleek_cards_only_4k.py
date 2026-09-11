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

img = Image.new("RGB", (width, height), "#FAFAFA")
draw = ImageDraw.Draw(img)

font_metric = ImageFont.truetype(font_bold_path, 60)
font_card_header = ImageFont.truetype(font_bold_path, 48)
font_card_desc = ImageFont.truetype(font_path, 38)
font_badge = ImageFont.truetype(font_bold_path, 34)

cards = [
    {
        "x1": 60, "y1": 60, "x2": 2340, "y2": 490,
        "accent": "#C8102E", "bg": "#FFFFFF", "border": "#FFCDD2",
        "badge": "OPTIMIZATION CORE", "badge_bg": "#FFEBEE", "badge_color": "#C8102E",
        "title": "Google OR-Tools MILP Solver",
        "desc": "Combinatorial mixed-integer linear programming core for multi-department block window clustering."
    },
    {
        "x1": 60, "y1": 530, "x2": 2340, "y2": 960,
        "accent": "#0D2B45", "bg": "#FFFFFF", "border": "#CFD8DC",
        "badge": "RAILWAY MANUAL", "badge_bg": "#ECEFF1", "badge_color": "#0D2B45",
        "title": "IRPWM Block Guidelines",
        "desc": "Complies strictly with Indian Railways Permanent Way Manual safety interlocks & minimum block durations."
    },
    {
        "x1": 60, "y1": 1000, "x2": 2340, "y2": 1430,
        "accent": "#E65100", "bg": "#FFFFFF", "border": "#FFE0B2",
        "badge": "LIVE CRIS APIS", "badge_bg": "#FFF3E0", "badge_color": "#E65100",
        "title": "CRIS COA & BDMS Feeds",
        "desc": "Direct integration with Control Office Application & Block Demand Management System real-time data feeds."
    },
    {
        "x1": 60, "y1": 1470, "x2": 2340, "y2": 1900,
        "accent": "#1565C0", "bg": "#FFFFFF", "border": "#BBDEFB",
        "badge": "AI LITERATURE", "badge_bg": "#E3F2FD", "badge_color": "#1565C0",
        "title": "Spatio-Temporal Graph NNs",
        "desc": "Predictive graph neural network models for real-time section bottleneck & loop line siding forecasting."
    }
]

for c in cards:
    draw.rounded_rectangle([c["x1"], c["y1"], c["x2"], c["y2"]], radius=24, fill=c["bg"], outline=c["border"], width=4)
    draw.rounded_rectangle([c["x1"] + 30, c["y1"] + 35, c["x1"] + 44, c["y2"] - 35], radius=6, fill=c["accent"])
    
    # Title
    draw.text((c["x1"] + 80, c["y1"] + 40), c["title"], font=font_card_header, fill="#0D2B45")
    
    # Badge Tag
    tb = font_badge.getbbox(c["badge"])
    tw = tb[2] - tb[0]
    bx1 = c["x2"] - 50 - tw - 40
    bx2 = c["x2"] - 50
    draw.rounded_rectangle([bx1, c["y1"] + 35, bx2, c["y1"] + 95], radius=14, fill=c["badge_bg"])
    draw.text((bx1 + 20, c["y1"] + 47), c["badge"], font=font_badge, fill=c["badge_color"])
    
    # Description
    lines = textwrap.wrap(c["desc"], width=68)
    dy = c["y1"] + 120
    for l in lines:
        draw.text((c["x1"] + 80, dy), l, font=font_card_desc, fill="#455A64")
        dy += 52

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide6_research_sleek_cards_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide6_research_sleek_cards_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("Sleek Slide 6 Research Cards generated successfully!")
