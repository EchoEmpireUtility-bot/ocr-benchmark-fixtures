# OCR Benchmark Fixtures

Controlled public fixtures for EchoEmpire Machine Foundry OCR Citation Chunker cloud benchmarking.

## Purpose

These PDFs exist only to provide stable, reproducible benchmark inputs for measuring:

- OCR runtime
- Apify compute usage
- memory usage
- OCR quality
- scaling behavior
- production pricing economics

They are separate from the OCR Citation Chunker product repository.

## Fixtures

### ocr-test-scan.pdf

- 1 page
- image-only scanned PDF
- no embedded text layer
- baseline clean OCR fixture
- used for startup-cost and single-page OCR benchmarking

## Benchmark Rule

Controlled cloud benchmarks that influence pricing must be preserved as named Apify datasets.

Disposable test runs remain unnamed.

Dataset naming convention:

`<product>-<purpose>-<version-or-case>`

### ocr-test-scan-10page.pdf

- 10 pages
- deterministic repetition of the verified 1-page image-only fixture
- no embedded text layer
- used to measure per-page OCR scaling against the 1-page baseline

### ocr-test-scan-25page.pdf

- 25 pages
- deterministic repetition of the verified 1-page image-only fixture
- no embedded text layer
- used to measure OCR scaling, memory headroom, and cloud cost at 512 MB

### ocr-test-scan-10page-noisy-mixed.pdf

- 10 image-only pages
- 4 clean control pages
- 1 reduced-contrast page
- 1 blurred page
- 1 resolution-degraded page
- 1 compounded low-contrast/blur page
- 2 blank image-only pages
- no embedded text layer
- generated deterministically by `make_mixed_fixture.py`
- used to measure OCR quality, blank-page behavior, and noisy-scan economics
