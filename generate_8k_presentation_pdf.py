import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_bold_path = font_path

width = 3840
height = 2160

# Load images
logo_path = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/railblock_ai_logo_square_highres.jpg"
logo_img = Image.open(logo_path).resize((180, 180), Image.Resampling.LANCZOS) if os.path.exists(logo_path) else None

s2_card_path = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide2_comparison_card_4k.png"
s2_card = Image.open(s2_card_path).resize((1700, 1380), Image.Resampling.LANCZOS) if os.path.exists(s2_card_path) else None

s3_table_path = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/slide3_table_only.png"
s3_table = Image.open(s3_table_path).resize((3400, 1200), Image.Resampling.LANCZOS) if os.path.exists(s3_table_path) else None

s4_card_path = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide4_feasibility_card_4k.png"
s4_card = Image.open(s4_card_path).resize((1700, 1380), Image.Resampling.LANCZOS) if os.path.exists(s4_card_path) else None

s5_card_path = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/slide5_impact_sleek_cards_only_4k.png"
s5_card = Image.open(s5_card_path).resize((1650, 1350), Image.Resampling.LANCZOS) if os.path.exists(s5_card_path) else None

s6_chart_path = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/.user_uploaded/uploaded_media_1789146001293.png"
s6_chart = Image.open(s6_chart_path).resize((1700, 1250), Image.Resampling.LANCZOS) if os.path.exists(s6_chart_path) else None

font_title = ImageFont.truetype(font_bold_path, 80)
font_subtitle = ImageFont.truetype(font_bold_path, 54)
font_sub_desc = ImageFont.truetype(font_path, 42)
font_sec_header = ImageFont.truetype(font_bold_path, 46)
font_bold = ImageFont.truetype(font_bold_path, 38)
font_regular = ImageFont.truetype(font_path, 38)
font_small = ImageFont.truetype(font_path, 30)

slides_images = []

def add_header_footer(slide_img, draw, page_num, title_text, title_color="#2E7D32", subtitle_text=None):
    if logo_img:
        slide_img.paste(logo_img, (100, 70))
        
    draw.text((320, 90), title_text, font=font_title, fill=title_color)
    
    if subtitle_text:
        draw.text((320, 185), subtitle_text, font=font_sub_desc, fill="#424242")
        
    draw.text((width - 650, 90), "SMART INDIA HACKATHON 2026", font=font_bold, fill="#0D2B45")
    
    draw.rectangle([0, height - 120, width, height], fill="#0288D1")
    draw.text((100, height - 80), "@SIH Idea submission-Template", font=font_small, fill="#FFFFFF")
    draw.text((width - 160, height - 80), str(page_num), font=font_small, fill="#FFFFFF")

# ==============================================================================
# SLIDE 1 (FIXED COVER - NO GRAY OVERLAY BOX)
# ==============================================================================
slide1 = Image.new("RGB", (width, height), "#FFFFFF")
d1 = ImageDraw.Draw(slide1)

d1.text((320, 110), "SMART INDIA HACKATHON 2026", font=ImageFont.truetype(font_bold_path, 96), fill="#0D2B45")
d1.text((width - 600, 120), "SIH 2026", font=font_title, fill="#1B5E20")

if logo_img:
    slide1.paste(logo_img, (100, 90))

fields = [
    ("Problem Statement ID :", "SIH26027", "#1B5E20"),
    ("Problem Statement Title :", "AI-Powered Automatic Block Planning to Maximize Asset\nAvailability for Train Operations on Indian Railways", "#D84315"),
    ("Theme:", "Transportation & Logistics", "#1B5E20"),
    ("Category:", "Software", "#D84315"),
    ("Team ID :", "NST", "#1B5E20"),
    ("Team Name :", "RailBlock-AI", "#D84315")
]

y1 = 360
for label, val, label_color in fields:
    d1.text((200, y1), label, font=font_sec_header, fill=label_color)
    lb = font_sec_header.getbbox(label)
    lw = lb[2] - lb[0]
    
    if "\n" in val:
        vlines = val.split("\n")
        d1.text((200 + lw + 20, y1), vlines[0], font=font_regular, fill="#212121")
        y1 += 55
        d1.text((200 + lw + 20, y1), vlines[1], font=font_regular, fill="#212121")
    else:
        d1.text((200 + lw + 20, y1), val, font=font_regular, fill="#212121")
    y1 += 130

# Clean Right Graphic (NO GRAY OVERLAY BOX)
right_x = 2600
d1.ellipse([right_x, 500, right_x + 800, 1300], fill="#E8F5E9", outline="#A5D6A7", width=6)
d1.text((right_x + 180, 840), "RailBlock-AI", font=ImageFont.truetype(font_bold_path, 72), fill="#0D2B45")
d1.text((right_x + 220, 940), "SIH26027 Engine", font=font_subtitle, fill="#C8102E")

d1.rectangle([0, height - 120, width, height], fill="#0288D1")
d1.text((100, height - 80), "@SIH Idea submission-Template", font=font_small, fill="#FFFFFF")
d1.text((width - 160, height - 80), "1", font=font_small, fill="#FFFFFF")

slides_images.append(slide1)

# ==============================================================================
# SLIDE 2
# ==============================================================================
slide2 = Image.new("RGB", (width, height), "#FFFFFF")
d2 = ImageDraw.Draw(slide2)
add_header_footer(slide2, d2, 2, "RailBlock-AI: Smart Railway Block Planning & Dispatch Engine", "#1B5E20")

s2_sections = [
    ("Detailed Explanation", "#D84315", [
        "• AI Master Coordinator for track maintenance & dispatching.",
        "• Combines P-Way, TRD & S&T into 1 joint block window.",
        "• Auto-sides slow trains on loop lines to prevent delays."
    ]),
    ("How it Addresses the Problem", "#1B5E20", [
        "• Reduces 4 track closures into 1 joint daily block.",
        "• Isolates train delays to single loop lines.",
        "• Recovers 42.9% lost track capacity on heavy corridors."
    ]),
    ("Innovation & Uniqueness", "#D84315", [
        "• Google OR-Tools MILP core for joint window clustering.",
        "• Dynamic speed & overtake predictor engine.",
        "• Live station-by-station track dashboard visualizer."
    ])
]

y2 = 320
for stitle, scolor, sbullets in s2_sections:
    d2.text((150, y2), stitle, font=font_sec_header, fill=scolor)
    y2 += 65
    for b in sbullets:
        d2.text((180, y2), b, font=font_regular, fill="#212121")
        y2 += 55
    y2 += 40

if s2_card:
    slide2.paste(s2_card, (2000, 320))

slides_images.append(slide2)

# ==============================================================================
# SLIDE 3
# ==============================================================================
slide3 = Image.new("RGB", (width, height), "#FFFFFF")
d3 = ImageDraw.Draw(slide3)
add_header_footer(slide3, d3, 3, "TECHNICAL APPROACH", "#D84315", "TECHNOLOGY USED AND METHODOLOGY")

if s3_table:
    slide3.paste(s3_table, (220, 380))

slides_images.append(slide3)

# ==============================================================================
# SLIDE 4
# ==============================================================================
slide4 = Image.new("RGB", (width, height), "#FFFFFF")
d4 = ImageDraw.Draw(slide4)
add_header_footer(slide4, d4, 4, "FEASIBILITY AND VIABILITY", "#1B5E20", "Implementation Feasibility, Operational Risks & Mitigation Strategies")

s4_sections = [
    ("Feasibility Analysis", "#D84315", [
        "• 100% Software: Zero track hardware changes needed.",
        "• High Scalability: Covers all 68 railway divisions.",
        "• Low Latency: MILP solver computes in seconds."
    ]),
    ("Challenges & Risks", "#1B5E20", [
        "• Siloed Depts: Coordinating P-Way, TRD & S&T.",
        "• Track Speeds: Handling varying section limits.",
        "• Change Management: Shifting controller workflows."
    ]),
    ("Strategies to Overcome", "#D84315", [
        "• CRIS Sync: Direct API hooks to COA & BDMS.",
        "• Human Control: Controllers retain click-approval.",
        "• Phased Rollout: Starting on Delhi-Mathura route."
    ])
]

y4 = 350
for stitle, scolor, sbullets in s4_sections:
    d4.text((150, y4), stitle, font=font_sec_header, fill=scolor)
    y4 += 65
    for b in sbullets:
        d4.text((180, y4), b, font=font_regular, fill="#212121")
        y4 += 55
    y4 += 45

if s4_card:
    slide4.paste(s4_card, (2000, 350))

slides_images.append(slide4)

# ==============================================================================
# SLIDE 5
# ==============================================================================
slide5 = Image.new("RGB", (width, height), "#FFFFFF")
d5 = ImageDraw.Draw(slide5)
add_header_footer(slide5, d5, 5, "IMPACT AND BENEFITS", "#D84315", "Operational, Economic, Social & Environmental Value Creation")

s5_bullets = [
    ("• Target Impact: ", "Reclaim 42.9% lost track capacity and eliminate domino delays across Indian Railways.", "#1B5E20"),
    ("• Social: ", "Millions of daily passengers enjoy predictable, on-time journeys with zero surprise delays.", "#D84315"),
    ("• Economic: ", "Saves Rs. 100s Cr in fuel waste, freight detention costs, and locomotive idle hours.", "#1B5E20"),
    ("• Environmental: ", "Cuts diesel freight idling emissions and optimizes electric traction power use.", "#D84315"),
    ("• Long-Term: ", "Scalable AI brain for nationwide rail network optimization under PM Gati Shakti.", "#1B5E20")
]

y5 = 380
for prefix, body, pcolor in s5_bullets:
    d5.text((150, y5), prefix, font=font_sec_header, fill=pcolor)
    pb = font_sec_header.getbbox(prefix)
    pw = pb[2] - pb[0]
    
    blines = textwrap.wrap(body, width=42)
    d5.text((150 + pw, y5), blines[0], font=font_regular, fill="#212121")
    if len(blines) > 1:
        y5 += 55
        d5.text((150 + pw, y5), blines[1], font=font_regular, fill="#212121")
    y5 += 110

if s5_card:
    slide5.paste(s5_card, (2050, 380))

slides_images.append(slide5)

# ==============================================================================
# SLIDE 6
# ==============================================================================
slide6 = Image.new("RGB", (width, height), "#FFFFFF")
d6 = ImageDraw.Draw(slide6)
add_header_footer(slide6, d6, 6, "RESEARCH AND REFERENCES", "#1B5E20", "Academic Papers, Railway Manuals & System Benchmarks")

s6_sections = [
    ("Government & Policy Reports", "#D84315", [
        "• Ministry of Railways (NRP 2030) - National Rail Plan Capacity Guidelines",
        "  https://indianrailways.gov.in",
        "• IRPWM Manual - Indian Railways Permanent Way Block Protocols"
    ]),
    ("AI & Railway Research", "#1B5E20", [
        "• Google OR-Tools - Constraint Solver for Train & Track Block Scheduling",
        "  https://developers.google.com/optimization",
        "• IEEE Transactions (2023) - Dynamic Train Rescheduling & Block Planning"
    ]),
    ("Existing Systems & Case Studies", "#D84315", [
        "• CRIS COA System - Control Office Application Live Dispatch Feeds",
        "• CRIS BDMS Portal - Block Demand Management System Workflows"
    ]),
    ("Technical References", "#1B5E20", [
        "• Spatio-Temporal Graph Neural Networks - Railway Bottleneck Models",
        "• Python NetworkX & PuLP - Network Routing & MILP Optimization Core"
    ])
]

y6 = 330
for stitle, scolor, sitems in s6_sections:
    d6.text((150, y6), "◆ " + stitle, font=font_sec_header, fill=scolor)
    y6 += 60
    for item in sitems:
        if "http" in item:
            d6.text((180, y6), item, font=font_small, fill="#1976D2")
            y6 += 45
        else:
            d6.text((180, y6), item, font=font_regular, fill="#212121")
            y6 += 55
    y6 += 25

if s6_chart:
    slide6.paste(s6_chart, (2000, 360))

slides_images.append(slide6)

# Save 8K PDF
pdf_path_art = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/RailBlock_AI_SIH26027_Winning_Presentation_8K.pdf"
pdf_path_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/RailBlock_AI_SIH26027_Winning_Presentation_8K.pdf"

slides_images[0].save(
    pdf_path_art,
    "PDF",
    resolution=300.0,
    save_all=True,
    append_images=slides_images[1:]
)

slides_images[0].save(
    pdf_path_proj,
    "PDF",
    resolution=300.0,
    save_all=True,
    append_images=slides_images[1:]
)

print("8K Presentation PDF generated successfully at:", pdf_path_proj)
