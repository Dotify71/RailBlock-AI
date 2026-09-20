from PIL import Image, ImageOps
import os

# Paths
hdr_path = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f/.user_uploaded/media_1789915731624.png"
content_path = "slide3_content_below_header_8k.png"

hdr_img = Image.open(hdr_path).convert("RGBA")
content_img = Image.open(content_path).convert("RGBA")

print("Header original size:", hdr_img.size)
print("Content original size:", content_img.size)

# Resize header to match content width (3840px) preserving aspect ratio
target_w = content_img.width
hdr_h = int(hdr_img.height * (target_w / hdr_img.width))
hdr_resized = hdr_img.resize((target_w, hdr_h), Image.Resampling.LANCZOS)

# Create blue footer bar (height ~ 90px at 3840w)
footer_h = 90
footer_img = Image.new("RGBA", (target_w, footer_h), (11, 60, 93, 255)) # #0B3C5D

# Combine canvas
total_h = hdr_resized.height + content_img.height + footer_img.height
combined_img = Image.new("RGBA", (target_w, total_h), (255, 255, 255, 255))

combined_img.paste(hdr_resized, (0, 0), hdr_resized)
combined_img.paste(content_img, (0, hdr_resized.height), content_img)
combined_img.paste(footer_img, (0, hdr_resized.height + content_img.height), footer_img)

out_combined = "slide3_full_with_exact_header_8k.png"
combined_img.save(out_combined, "PNG")
print(f"Saved combined full slide: {out_combined} with dimensions ({target_w}x{total_h})")

# Copy to artifacts
artifacts_dir = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f"
if os.path.exists(artifacts_dir):
    os.system(f"cp {out_combined} {artifacts_dir}/")
    print("Copied slide3_full_with_exact_header_8k.png to brain artifacts directory!")
