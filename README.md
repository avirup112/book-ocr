# Book OCR — Information Extraction Pipeline 📚🔍

**Short description**

A lightweight OCR pipeline that processes book cover / page images, performs OCR (EasyOCR or Tesseract), and extracts structured metadata (title, author, ISBN, publisher, year, etc.). This repository includes image preprocessing, multiple OCR engine support, and extraction heuristics to save results as JSON.

---

## Features ✅

- Image preprocessing (denoise, thresholding) 🔧
- Two OCR engine backends: **EasyOCR** and **Tesseract** 🧠
- Metadata extraction using regex/patterns (ISBN, year, pages, price, title, author) ✂️
- Batch processing and single-image modes with JSON output 📄
- Simple logging and output organization 📁

---

## Quick start — Run locally ⚡

1. Create and activate a Python virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) If you want to use Tesseract OCR, install the Tesseract engine on your OS (system package). On Windows, install Tesseract and ensure the `tesseract` binary is on your PATH.

4. Add input images to `data/input/` (supported extensions: .jpg, .jpeg, .png, .bmp, .tiff)

5. Run the main script:

```bash
python main.py
```

This runs the default *process all images* flow. Results are saved in `data/output/` as `batch_results_YYYYMMDD_HHMMSS.json` and processed images are stored in `data/processed/`.

---

## Configuration 🔧

- `config.py` contains the main configuration (paths, OCR engine, language, preprocessing parameters, logging settings).
- Key fields:
  - `INPUT_DIR` — `data/input`
  - `OUTPUT_DIR` — `data/output`
  - `PROCESSED_DIR` — `data/processed`
  - `OCR_ENGINE` — set to `"easyocr"` (default) or `"tesseract"`
  - `OCR_LANGUAGES` — e.g., `["en"]`

You can edit `config.py` to change OCR engine, thresholds, or directories.

---

## Usage modes 🔁

- Process all images automatically (default): runs `BookOCR.process_all_images()` and produces timestamped JSON output.
- Process a specific list of images: call `BookOCR.process_batch(image_paths, output_file=..., save_processed=True)`.
- Process a single image: call `BookOCR.process_image(image_path, save_processed=True)`.

The `main.py` file includes commented examples for batch and single-image usage.

---

## Output format 📝

The JSON output contains an array of extracted records. Each record is a dictionary representation of `models.BookMetadata`, for example:

```json
{
  "title": "Example Book Title",
  "author": "Jane Doe",
  "isbn_13": "9781234567897",
  "publication_year": "2019",
  "confidence": 0.83
}
```

---

## Project structure 📂

- `main.py` — pipeline orchestration and CLI-like entrypoint
- `config.py` — configuration and default directories
- `requirements.txt` — Python dependencies
- `data/` — input and output folders:
  - `data/input/` — put images here
  - `data/output/` — JSON results are written here
  - `data/processed/` — processed images saved here
- `ocr/` — OCR engines:
  - `easyocr_engine.py` — EasyOCR wrapper
  - `tesseract_engine.py` — pytesseract wrapper
- `preprocessing/` — image preprocessing utilities
- `extraction/` — information extraction (patterns + extractor)
- `models/` — data models (`BookMetadata`)
- `utils/` — logging utilities
- `logs/` — runtime logs (created automatically)

---

## Notes & tips 💡

- If `easyocr` isn't available the code falls back to the configured Tesseract engine (and vice versa if you change `OCR_ENGINE`).
- Tesseract requires a system install (not just the `pytesseract` Python package). Make sure the executable is in PATH.
- Preprocessing parameters are in `config.py` and can be tuned for different image qualities.

---

## Contributing & license 🤝

- Feel free to open issues or submit PRs to improve extraction rules or add more OCR features.
- No license file is included — add a LICENSE if you want to publish under a specific license.

---
