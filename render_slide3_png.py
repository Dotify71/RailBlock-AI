import asyncio
from playwright.async_api import async_playwright
import os
from PIL import Image

async def render_slide():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Create page with 16:9 4K viewport (3840x2160)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=2)
        
        file_url = "file://" + os.path.abspath("generate_slide3_architecture.html")
        await page.goto(file_url)
        await page.wait_for_timeout(1000) # Ensure fonts render
        
        full_slide_path = "slide3_architecture_8k.png"
        await page.screenshot(path=full_slide_path)
        print(f"Rendered full slide image: {full_slide_path}")
        
        # Also render content-only element (main-content area below header)
        content_element = await page.query_selector(".main-content")
        content_only_path = "slide3_content_below_header_8k.png"
        if content_element:
            await content_element.screenshot(path=content_only_path)
            print(f"Rendered content-only image: {content_only_path}")

        await browser.close()

    # Also copy to artifacts directory
    artifacts_dir = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f"
    if os.path.exists(artifacts_dir):
        os.system(f"cp {full_slide_path} {artifacts_dir}/")
        os.system(f"cp {content_only_path} {artifacts_dir}/")
        print("Copied images to brain artifacts directory!")

if __name__ == "__main__":
    asyncio.run(render_slide())
