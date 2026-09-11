import generate_8k_presentation_pdf
from PIL import Image

output_png = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/page1_fixed_preview.png"
generate_8k_presentation_pdf.slides_images[0].save(output_png, "PNG")
print("Page 1 fixed preview saved successfully:", output_png)
