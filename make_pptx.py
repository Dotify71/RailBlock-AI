"""
RailBlock-AI Presentation Generator
Creates official 6-slide PowerPoint presentation deck (.pptx) for SIH 2026 PS SIH26027
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation(output_path):
    prs = Presentation()
    
    # Set slide dimensions to widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    blank_slide_layout = prs.slide_layouts[6]
    
    # Colors
    NAVY = RGBColor(11, 37, 69)
    AMBER = RGBColor(245, 158, 11)
    SLATE = RGBColor(30, 41, 59)
    WHITE = RGBColor(255, 255, 255)
    EMERALD = RGBColor(16, 185, 129)
    RED = RGBColor(220, 38, 38)
    
    def add_header(slide, title_text, category_text="SIH 2026 | PS ID: SIH26027 | Ministry of Railways"):
        # Top banner background
        top_bar = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.2)) # rect
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = NAVY
        top_bar.line.fill.background()
        
        # Sub status stripe
        sub_bar = slide.shapes.add_shape(1, Inches(0), Inches(1.2), Inches(13.333), Inches(0.3))
        sub_bar.fill.solid()
        sub_bar.fill.fore_color.rgb = AMBER
        sub_bar.line.fill.background()
        
        # Title text
        txBox = slide.shapes.add_textbox(Inches(0.6), Inches(0.15), Inches(12), Inches(0.9))
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        p2 = tf.add_paragraph()
        p2.text = category_text
        p2.font.size = Pt(13)
        p2.font.color.rgb = AMBER

    # SLIDE 1: Title Slide
    slide1 = prs.slides.add_slide(blank_slide_layout)
    bg1 = slide1.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()
    
    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "RailBlock-AI"
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = AMBER
    
    p = tf1.add_paragraph()
    p.text = "AI-Powered Automatic Block Planning & Dynamic Train Dispatching System for Indian Railways"
    p.font.size = Pt(22)
    p.font.color.rgb = WHITE
    p.font.bold = True
    
    p = tf1.add_paragraph()
    p.text = "\nProblem Statement ID: SIH26027  |  Theme: Transportation & Logistics  |  Category: Software\nSponsoring Organization: Ministry of Railways"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(203, 213, 225)
    
    p = tf1.add_paragraph()
    p.text = "\nTeam Name: TrackTech Innovators  |  College Internal Hackathon Submission"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    # SLIDE 2: Problem Statement & Existing Bottlenecks
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "1. Problem Statement & Existing Bottlenecks")
    
    tb2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "Current Operational Bottleneck in Indian Railways:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = SLATE
    
    bullets = [
        ("Decentralized Department Requests:", "P-Way (Tracks), TRD (Electrification), and S&T (Signals) file separate maintenance block requests in BDMS."),
        ("Repeated Track Closures:", "The same section is closed 3 to 4 times a day, causing 14+ hours of track downtime."),
        ("Severe Train Detentions:", "Trains behind a delayed train get stuck in a queue due to manual, phone-based loop line siding decisions."),
        ("Wasted Capacity:", "Over 40% of track capacity is wasted every day due to uncoordinated maintenance and cascading delays.")
    ]
    for title, body in bullets:
        p = tf2.add_paragraph()
        p.text = f"• {title} {body}"
        p.font.size = Pt(16)
        p.font.color.rgb = SLATE
        p.space_after = Pt(12)

    # SLIDE 3: Proposed Solution & Technical Architecture
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "2. Proposed Solution: RailBlock-AI Platform")
    
    tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    
    p = tf3.paragraphs[0]
    p.text = "Dual-Engine AI Architecture:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = SLATE
    
    solutions = [
        ("Feature 1: Joint Department Maintenance Windows:", "Clustering P-Way, TRD, and S&T requests into ONE single 4-hour window using Google OR-Tools (MILP Optimization)."),
        ("Feature 2: AI Train Dispatcher & Overtake Engine:", "Real-time siding of slow/delayed trains on Station Loop Lines to allow high-priority express trains (Rajdhani / Vande Bharat) to overtake on Main Line with ZERO delay."),
        ("Tech Stack:", "Python (FastAPI + OR-Tools), React.js / Tailwind CSS, 'Where Is My Train' Style Route Visualizer."),
        ("Passenger Advisory Portal:", "Transparent public warning dashboard for 2.3 crore daily Indian passengers.")
    ]
    for title, body in solutions:
        p = tf3.add_paragraph()
        p.text = f"• {title} {body}"
        p.font.size = Pt(16)
        p.font.color.rgb = SLATE
        p.space_after = Pt(12)

    # SLIDE 4: Feature 1 vs Feature 2 Deep Dive
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "3. Feature Breakdown & Operations Flow")
    
    tb4 = slide4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    
    p = tf4.paragraphs[0]
    p.text = "Detailed System Operations:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = SLATE
    
    details = [
        ("Joint Maintenance Windows:", "Instead of 5 shutdowns (14h), RailBlock-AI outputs 2 joint windows (8h), recovering 42.9% track capacity."),
        ("Loop Line Siding Directive:", "Example: Container Freight G-501 held at Palwal (PWL) Loop Line 2 for 12 mins -> Saved 50 Mins cascading delay across 12004 Shatabdi & 12952 Rajdhani."),
        ("Safety Buffer Compliance:", "Mandatory track clearance time and speed restriction protocols strictly enforced by AI constraint model."),
        ("CRIS Integration Ready:", "Designed to connect directly with CRIS (COA & BDMS) APIs.")
    ]
    for title, body in details:
        p = tf4.add_paragraph()
        p.text = f"• {title} {body}"
        p.font.size = Pt(16)
        p.font.color.rgb = SLATE
        p.space_after = Pt(12)

    # SLIDE 5: Expected Business Impact & Key Metrics
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "4. Expected Business & Operational Impact")
    
    tb5 = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    
    p = tf5.paragraphs[0]
    p.text = "Key Performance Indicators (KPIs):"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = SLATE
    
    kpis = [
        ("+42.9% Track Capacity Recovered:", "Eliminates redundant track closures across all 68 railway divisions."),
        ("6.0 Hours Shutdown Saved Daily:", "Significant reduction in train detention hours per division."),
        ("50+ Mins Cascading Delay Prevented:", "Isolates delays to single trains without affecting trailing express trains."),
        ("Zero Cross-Department Conflicts:", "100% automated coordination between P-Way, TRD, and S&T.")
    ]
    for title, body in kpis:
        p = tf5.add_paragraph()
        p.text = f"• {title} {body}"
        p.font.size = Pt(16)
        p.font.color.rgb = SLATE
        p.space_after = Pt(12)

    # SLIDE 6: Implementation Roadmap & Prototype Status
    slide6 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide6, "5. Implementation Roadmap & Prototype Status")
    
    tb6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.2))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    
    p = tf6.paragraphs[0]
    p.text = "Prototype Status & SIH 2026 Roadmap:"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = SLATE
    
    steps = [
        ("Working Prototype Delivered:", "Dual-engine Python API backend + interactive 'Where Is My Train' style web dashboard fully functional."),
        ("Data Strategy:", "Currently running on simulated Delhi-Mathura-Agra division datasets; ready to integrate with CRIS sandbox APIs."),
        ("Scalability:", "Cloud-native modular architecture scalable to all Indian Railway zones (NR, NCR, WCR, etc.)."),
        ("Finals Preparation:", "Team ready to demonstrate live constraint solver and interactive dispatch map in 36-hour hackathon.")
    ]
    for title, body in steps:
        p = tf6.add_paragraph()
        p.text = f"• {title} {body}"
        p.font.size = Pt(16)
        p.font.color.rgb = SLATE
        p.space_after = Pt(12)
        
    prs.save(output_path)
    print(f"✅ Presentation saved to {output_path}")

if __name__ == "__main__":
    out_file = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/RailBlock_AI_SIH26027_Presentation.pptx"
    create_presentation(out_file)
