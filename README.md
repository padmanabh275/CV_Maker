# CV_Maker – Update CVs from scanned PDFs/images

A Python-based tool to **upload an existing CV** (PDF or image), **extract and update key details** (position, company, phone, etc.), and **generate a clean, ATS-friendly CV** in DOCX (and optionally PDF).

---

## Features

- **Upload** – PDF or image (PNG/JPG) of an existing CV
- **Extract** – Text from PDF (`pdfplumber`) or OCR from images (`pytesseract` + Pillow)
- **Structured parsing** – Detects Name, DOB, Career Objective, Experience (company, role, dates, duties), and strips boilerplate
- **Simple form** – Enter/confirm Name, Email, Location, Position, Current company, Current position, Phone
- **One-click generate** – Builds a professional, single-column CV with consistent styling
- **Output** – DOCX (and optionally PDF via `docx2pdf` if Word is available)

---

## Setup

Use the `torch_env` conda environment (or create it):

```bash
conda create -n torch_env python=3.10
conda activate torch_env
pip install -r requirements.txt
```

**Requirements:** `pdfplumber`, `pytesseract`, `Pillow`, `python-docx`, `streamlit`. For PDF export: `docx2pdf` (needs Microsoft Word on Windows).

**Tesseract:** For image/OCR support, install [Tesseract](https://github.com/tesseract-ocr/tesseract) and ensure it’s on your PATH.

---

## Quick start (Streamlit UI)

1. Start the app:
   ```bash
   conda run -n torch_env streamlit run app.py
   ```
2. Open the URL (e.g. `http://localhost:8501`).
3. **Upload** a CV (PDF or image).
4. Click **“Pick up details from this CV”** to pre-fill name, email, phone, skills (and optionally show extracted text).
5. Enter or edit **Name**, **Email**, **Location**, **Position**, **Current company**, **Current position**, **Phone**.
6. Click **“Generate New CV”** and **Download DOCX**.

---

## CLI (optional)

Generate a CV from a profile JSON and optional input PDF:

```bash
conda run -n torch_env python main.py --input path\to\cv.pdf --profile profiles\example_profile.json --output-docx output\updated_cv.docx [--output-pdf]
```

---

## Generated CV structure (ATS-friendly)

- **Header** – Name (centered), Contact line (Phone · Email · Location · DOB), Current position at company
- **Career Objective** – Parsed from uploaded CV (single paragraph)
- **Professional Summary** – From current position/company or profile
- **Experience & Background** – Cleaned full content with bullets for duties; declaration/sign-off and duplicate header fields removed
- **Work Experience** – Structured entries (company, role, dates, bullets) when parsed
- **Education** – When present in profile
- **Skills** – Bullet list

Boilerplate (Resume, CAREER OBJECTIVE headers, etc.), duplicate contact/DOB lines, declaration (“I hereby solemnly declare…”), and sign-off (“Your Faithfully”, “Mr. …”) are stripped for a clean, professional output.

---

## Project layout

| File / folder      | Purpose |
|--------------------|--------|
| `app.py`           | Streamlit UI: upload, form, generate, download |
| `main.py`          | CV parsing, cleaning, DOCX building, CLI |
| `profiles/`        | Example profile JSON |
| `requirements.txt` | Python dependencies |
| `Current_Status.md`| Snapshot of current features and status (for reference) |

---

## Reference

- **Current status and feature list** – See [Current_Status.md](Current_Status.md).
