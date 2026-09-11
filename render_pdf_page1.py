from PIL import Image

pdf_path = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/RailBlock_AI_SIH26027_Winning_Presentation_8K.pdf"

# Open Page 1 from generated PDF
img = Image.open(pdf_path)
img.seek(0)
output_png = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/page1_fixed_preview.png"
img.save(output_png, "PNG")
print("Page 1 preview saved:", output_png)
