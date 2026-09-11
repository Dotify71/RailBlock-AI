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

font_metric = ImageFont.truetype(font_bold_path, 96)
font_card_header = ImageFont.truetype(font_bold_path, 48)
font_card_desc = ImageFont.truetype(font_path, 38)

cards = [
    {
        "x1": 60, "y1": 60, "x2": 1160, "y2": 940,
        "accent": "#C8102E", "bg": "#FFFFFF", "border": "#FFCDD2",
        "metric": "42.9%",
        "title": "Track Capacity Reclaimed",
        "desc": "Consolidates multi-departmental P-Way, TRD & S&T maintenance requests into 1 single joint daily block window."
    },
    {
        "x1": 1240, "y1": 60, "x2": 2340, "y2": 940,
        "accent": "#0D2B45", "bg": "#FFFFFF", "border": "#CFD8DC",
        "metric": "Rs. 100s Cr",
        "title": "Annual Economic Savings",
        "desc": "Prevents locomotive idle hours, reduces diesel freight detention costs, and eliminates wasted track downtime."
    },
    {
        "x1": 60, "y1": 1020, "x2": 1160, "y2": 1900,
        "accent": "#E65100", "bg": "#FFFFFF", "border": "#FFE0B2",
        "metric": "Zero Delay",
        "title": "Passenger Punctuality",
        "desc": "Isolates slow train holds to station loop lines, allowing fast express passenger trains to run at full speed."
    },
    {
        "x1": 1240, "y1": 1020, "x2": 2340, "y2": 1900,
        "accent": "#1565C0", "bg": "#FFFFFF", "border": "#BBDEFB",
        "metric": "NRP 2030",
        "title": "PM Gati Shakti Scalability",
        "desc": "Cloud-native AI brain designed for seamless deployment across all 68 Indian Railway divisions nationwide."
    }
]

for c in cards:
    draw.rounded_rectangle([c["x1"], c["y1"], c["x2"], c["y2"]], radius=28, fill=c["bg"], outline=c["border"], width=4)
    draw.rounded_rectangle([c["x1"] + 30, c["y1"] + 40, c["x1"] + 44, c["y2"] - 40], radius=6, fill=c["accent"])
    
    draw.text((c["x1"] + 80, c["y1"] + 60), c["metric"], font=font_metric, fill=c["accent"])
    draw.text((c["x1"] + 80, c["y1"] + 200), c["title"], font=font_card_header, fill="#0D2B45")
    
    lines = textwrap.wrap(c["desc"], width=40)
    dy = c["y1"] + 280
    for l in lines:
        draw.text((c["x1"] + 80, dy), l, font=font_card_desc, fill="#455A64")
        dy += 54

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide5_impact_sleek_cards_only_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide5_impact_sleek_cards_only_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("Sleek Cards-Only 4K Slide 5 image generated successfully!")
