import os
import re
import time
import img2pdf
from playwright.sync_api import sync_playwright
import argparse

URL = "https://slide-ds.zhongpu.info/week3"
TOTAL_SLIDES_DEFAULT = 20

def detect_total_slides(page, default=TOTAL_SLIDES_DEFAULT):
    try:
        locator = page.get_by_text(re.compile(r"\b\d+\s*/\s*\d+\b"))
        texts = locator.all_text_contents()
        for t in texts:
            m = re.search(r"(\d+)\s*/\s*(\d+)", t)
            if m:
                return int(m.group(2))
    except Exception:
        pass
    try:
        content = page.content()
        m = re.search(r"(\d+)\s*/\s*(\d+)", content)
        if m:
            return int(m.group(2))
    except Exception:
        pass
    return default

def main(url=URL, out_path="Slidev_Presentation_week3.pdf", temp_dir="temp"):
    os.makedirs(temp_dir, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(url, wait_until="networkidle")
        page.add_style_tag(content="""
            *[class*="icon-btn"] { display: none !important; }
            *[class*="slidev-controls"] { display: none !important; }
            .controls, .toolbar, .nav, .remote-controls { display: none !important; }
        """)
        total = detect_total_slides(page, default=TOTAL_SLIDES_DEFAULT)
        for i in range(1, total + 1):
            page.screenshot(path=f"{temp_dir}/slide_{i}.png")
            if i < total:
                page.keyboard.press("ArrowRight")
                time.sleep(1)
        with open(out_path, "wb") as f:
            f.write(img2pdf.convert([f"{temp_dir}/slide_{i}.png" for i in range(1, total + 1)]))
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="?", default=URL)
    parser.add_argument("--out", default="Slidev_Presentation_week3.pdf")
    parser.add_argument("--tempdir", default="temp")
    args = parser.parse_args()
    main(url=args.url, out_path=args.out, temp_dir=args.tempdir)

