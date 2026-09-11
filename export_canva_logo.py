import os
from PIL import Image, ImageDraw, ImageFont

# Load fonts
font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"

font_logo = ImageFont.truetype(font_path, 40)
font_sub = ImageFont.truetype(font_path, 20)

# 1. Circular / Square Badge Logo for Top-Left Canva Header (500x500 PNG)
width, height = 500, 500
img_badge = Image.new("RGBA", (width, height), (0, 0, 0, 0)) # Transparent background
draw = ImageDraw.Draw(img_badge)

# Draw Railway Red Circle with Navy Ring
draw.ellipse([20, 20, 480, 480], fill="#C8102E", outline="#0D2B45", width=12)

# Draw Train Track Icon / Emblems
draw.rectangle([210, 80, 290, 420], fill="#FFFFFF") # Track line left
draw.rectangle([130, 180, 370, 210], fill="#FFFFFF") # Sleeper 1
draw.rectangle([130, 250, 370, 280], fill="#FFFFFF") # Sleeper 2
draw.rectangle([130, 320, 370, 350], fill="#FFFFFF") # Sleeper 3
draw.polygon([(250, 100), (390, 390), (110, 390)], outline="#0D2B45", width=8) # AI Network Overlay

# 2. Horizontal Header Logo (800x250 PNG with White Background)
w_h, h_h = 800, 250
img_horiz = Image.new("RGBA", (w_h, h_h), (255, 255, 255, 255))
draw_h = ImageDraw.Draw(img_horiz)

# Icon Badge on Left
draw_h.ellipse([30, 25, 225, 220], fill="#C8102E", outline="#0D2B45", width=6)
draw_h.rectangle([115, 65, 140, 180], fill="#FFFFFF")
draw_h.rectangle([80, 100, 175, 115], fill="#FFFFFF")
draw_h.rectangle([80, 135, 175, 150], fill="#FFFFFF")

# Text on Right
draw_h.text((250, 65), "RailBlock-AI", font=font_logo, fill="#0D2B45")
draw_h.text((250, 125), "Smart Railway Block Engine", font=font_sub, fill="#C8102E")
draw_h.text((250, 160), "SIH 2026 | Ministry of Railways", font=font_sub, fill="#1B5E20")

# Save outputs to artifacts & project folder
path1 = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/railblock_logo_badge.png"
path2 = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/railblock_logo_horizontal.png"

proj_path1 = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/railblock_logo_badge.png"
proj_path2 = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/railblock_logo_horizontal.png"

img_badge.save(path1, "PNG")
img_badge.save(proj_path1, "PNG")

img_horiz.save(path2, "PNG")
img_horiz.save(proj_path2, "PNG")

print("Canva PNG Logos exported successfully!")
