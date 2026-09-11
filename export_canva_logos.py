import os
import shutil
from PIL import Image

assets_dir = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/frontend/assets"
art_dir = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f"

src_app_icon = os.path.join(assets_dir, "railblock_ai_app_icon_1788977979726.jpg")
src_dark = os.path.join(assets_dir, "railblock_ai_refined_dark_1788978639407.jpg")
src_horiz = os.path.join(assets_dir, "railblock_ai_refined_horizontal_1788978601991.jpg")

dest_icon = os.path.join(art_dir, "railblock_ai_logo_square_highres.jpg")
dest_icon_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/railblock_ai_logo_square_highres.jpg"

if os.path.exists(src_app_icon):
    shutil.copy(src_app_icon, dest_icon)
    shutil.copy(src_app_icon, dest_icon_proj)
    print("Copied original high-res square logo to:", dest_icon)

dest_horiz = os.path.join(art_dir, "railblock_ai_logo_horizontal_highres.jpg")
dest_horiz_proj = "/Users/dushyantacharya/Documents/PROJECTS/Fighter/antigravity-game/railblock-ai/railblock_ai_logo_horizontal_highres.jpg"

if os.path.exists(src_horiz):
    shutil.copy(src_horiz, dest_horiz)
    shutil.copy(src_horiz, dest_horiz_proj)
    print("Copied original high-res horizontal logo to:", dest_horiz)

