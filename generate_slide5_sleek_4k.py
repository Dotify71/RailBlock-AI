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

font_title = ImageFont.truetype(font_bold_path, 72)
font_subtitle = ImageFont.truetype(font_path, 42)
font_metric = ImageFont.truetype(font_bold_path, 90)
font_card_header = ImageFont.truetype(font_bold_path, 46)
font_card_desc = ImageFont.truetype(font_path, 36)

# Title (Clean Railway Navy & Red, NO GREEN BANNER)
draw.text((80, 70), "QUANTIFIABLE IMPACT & VALUE", font=font_title, fill="#0D2B45")
draw.text((80, 155), "RailBlock-AI Operational, Economic & Commuter Benefits", font=font_subtitle, fill="#546E7A")

# Subtle Top Accent Bar (Railway Red & Navy)
draw.rectangle([80, 220, 380, 228], fill="#C8102E")
draw.rectangle([390, 220, 690, 228], fill="#0D2B45")

cards = [
    {
        "x1": 80, "y1": 270, "x2": 1160, "y2": 1050,
        "accent": "#C8102E", "bg": "#FFFFFF", "border": "#FFCDD2",
        "metric": "42.9%",
        "title": "Track Capacity Reclaimed",
        "desc": "Consolidates multi-departmental P-Way, TRD & S&T maintenance requests into 1 single joint daily block window."
    },
    {
        "x1": 1240, "y1": 270, "x2": 2320, "y2": 1050,
        "accent": "#0D2B45", "bg": "#FFFFFF", "border": "#CFD8DC",
        "metric": "Rs. 100s Cr",
        "title": "Annual Economic Savings",
        "desc": "Prevents locomotive idle hours, reduces diesel freight detention costs, and eliminates wasted track downtime."
    },
    {
        "x1": 80, "y1": 1110, "x2": 1160, "y2": 1890,
        "accent": "#E65100", "bg": "#FFFFFF", "border": "#FFE0B2",
        "metric": "Zero Delay",
        "title": "Passenger Punctuality",
        "desc": "Isolates slow train holds to station loop lines, allowing fast express passenger trains to run at full speed."
    },
    {
        "x1": 1240, "y1": 1110, "x2": 2320, "y2": 1890,
        "accent": "#1565C0", "bg": "#FFFFFF", "border": "#BBDEFB",
        "metric": "NRP 2030",
        "title": "PM Gati Shakti Scalability",
        "desc": "Cloud-native AI brain designed for seamless deployment across all 68 Indian Railway divisions nationwide."
    }
]

for c in cards:
    # Outer Card Box
    draw.rounded_rectangle([c["x1"], c["y1"], c["x2"], c["y2"]], radius=28, fill=c["bg"], outline=c["border"], width=4)
    
    # Left Accent Bar inside Card
    draw.rounded_rectangle([c["x1"] + 30, c["y1"] + 40, c["x1"] + 44, c["y2"] - 40], radius=6, fill=c["accent"])
    
    # Metric Number
    draw.text((c["x1"] + 80, c["y1"] + 60), c["metric"], font=font_metric, fill=c["accent"])
    
    # Card Title
    draw.text((c["x1"] + 80, c["y1"] + 190), c["title"], font=font_card_header, fill="#0D2B45")
    
    # Description Text
    lines = textwrap.wrap(c["desc"], width=40)
    dy = c["y1"] + 270
    for l in lines:
        draw.text((c["x1"] + 80, dy), l, font=font_card_desc, fill="#455A64")
        dy += 54

output_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide5_impact_sleek_4k.png"
output_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide5_impact_sleek_4k.png"

img.save(output_art, "PNG", dpi=(300, 300))
img.save(output_proj, "PNG", dpi=(300, 300))
print("Sleek 4K Slide 5 Card generated successfully!")
