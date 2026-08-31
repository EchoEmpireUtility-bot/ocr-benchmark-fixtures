"""Create the deterministic 50-page clean OCR benchmark fixture."""

from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "ocr-test-scan.pdf"
OUTPUT = ROOT / "clean-scan-50-page.pdf"
PAGE_COUNT = 50


def main() -> None:
    source = fitz.open(SOURCE)
    page = source[0]
    rect = page.rect

    # Match the existing fixture-generation method: rasterize the one-page
    # clean control and embed an identical PNG on every output page.
    pix = page.get_pixmap(dpi=200, alpha=False)
    image = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")

    output = fitz.open()
    for _ in range(PAGE_COUNT):
        buffer = BytesIO()
        image.save(buffer, format="PNG", optimize=False)
        new_page = output.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(new_page.rect, stream=buffer.getvalue())

    output.save(OUTPUT, garbage=4, deflate=True)
    output.close()
    source.close()
    print(f"created={OUTPUT.name}")
    print(f"pages={PAGE_COUNT}")


if __name__ == "__main__":
    main()
