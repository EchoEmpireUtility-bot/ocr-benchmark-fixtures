from io import BytesIO

import fitz
from PIL import Image, ImageEnhance, ImageFilter

SOURCE = "ocr-test-scan.pdf"
OUTPUT = "ocr-test-scan-10page-noisy-mixed.pdf"

src = fitz.open(SOURCE)
page = src[0]
rect = page.rect

pix = page.get_pixmap(dpi=200, alpha=False)
base = Image.open(BytesIO(pix.tobytes("png"))).convert("RGB")

pages = []

# 1-4: clean controls
for _ in range(4):
    pages.append(base.copy())

# 5: reduced contrast
pages.append(ImageEnhance.Contrast(base).enhance(0.45))

# 6: mild blur
pages.append(base.filter(ImageFilter.GaussianBlur(radius=1.4)))

# 7: resolution degradation
small = base.resize(
    (max(1, base.width // 2), max(1, base.height // 2)),
    Image.Resampling.BILINEAR,
)
pages.append(
    small.resize(base.size, Image.Resampling.BILINEAR)
)

# 8: compounded low contrast + blur
degraded = ImageEnhance.Contrast(base).enhance(0.35)
degraded = degraded.filter(ImageFilter.GaussianBlur(radius=1.8))
pages.append(degraded)

# 9-10: truly blank image-only pages
blank = Image.new("RGB", base.size, "white")
pages.append(blank.copy())
pages.append(blank.copy())

out = fitz.open()

for image in pages:
    buf = BytesIO()
    image.save(buf, format="PNG", optimize=False)

    new_page = out.new_page(width=rect.width, height=rect.height)
    new_page.insert_image(new_page.rect, stream=buf.getvalue())

out.save(OUTPUT, garbage=4, deflate=True)
out.close()
src.close()

print(f"created={OUTPUT}")
print(f"pages={len(pages)}")
