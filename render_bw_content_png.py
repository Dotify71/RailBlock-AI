import asyncio
from playwright.async_api import async_playwright
import os

async def render_bw_slide():
    # First generate HTML
    os.system("python3 generate_bw_content.py")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 950}, device_scale_factor=2)
        
        file_url = "file://" + os.path.abspath("slide3_bw_content.html")
        await page.goto(file_url)
        await page.wait_for_timeout(1000)
        
        element = await page.query_selector(".main-content")
        out_path = "slide3_content_bw_8k.png"
        
        if element:
            await element.screenshot(path=out_path)
            print(f"Rendered Black & White content-only 8K image: {out_path}")
        else:
            await page.screenshot(path=out_path)
            print(f"Rendered full B&W page: {out_path}")

        await browser.close()

    # Copy to brain artifacts
    artifacts_dir = "/Users/dushyantacharya/.gemini/antigravity/brain/3e27fecf-19d5-4c17-9432-ffa2ce99e25f"
    if os.path.exists(artifacts_dir):
        os.system(f"cp {out_path} {artifacts_dir}/")
        print("Copied slide3_content_bw_8k.png to brain artifacts directory!")

if __name__ == "__main__":
    asyncio.run(render_bw_slide())
