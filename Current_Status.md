# CV_Maker – Current Status

*Snapshot for quick reference. Last updated to match the codebase as of the latest changes.*

---

## What’s implemented

### 1. Input and extraction
- **Upload:** PDF or image (PNG, JPG, JPEG).
- **PDF:** Text extraction via `pdfplumber`.
- **Image:** OCR via `pytesseract` + Pillow.
- **“Pick up details from this CV”** in the UI runs extraction and parses into structured fields.

### 2. Parsing and structured fields
- **Name** – From “Name :” or first line.
- **DOB** – From “DOB :” / “Date of Birth :”.
- **Career Objective** – Paragraph after “Career Objective” / “Objective”; stops at “Personal information”, “Name :”, etc., so it doesn’t include the rest of the CV.
- **Experience** – After “Experience” / “Work Experience”, or from “Company Name :- X” when no section header exists. Extracts company, location, dates, role (e.g. Associate Technician), and duty lines.
- **Skills** – From a “Skills” section in the extracted text.
- **Label : value** – Name, DOB, etc. read from “Label : value” lines.

### 3. Streamlit UI (`app.py`)
- File upload (PDF/image).
- Button to “Pick up details from this CV” (fills name, email, phone, skills from extraction).
- Optional display of extracted CV text.
- Form: Name, Email, Location, Position (dropdown + custom), Current company, Current position, Phone.
- “Generate New CV” builds the DOCX and shows a download button.

### 4. Generated CV content and layout (`main.py`)
- **ATS-style layout:** Single column, Calibri, clear headings with underlines, 1” margins, 1.15 line spacing.
- **Sections (in order):**
  - Header (name, contact line with DOB, current position at company).
  - Horizontal divider.
  - Career Objective (parsed paragraph only).
  - Professional Summary.
  - Experience & Background (reorganized, with bullets for duties).
  - Work Experience (structured entries when parsing provides them).
  - Education (from profile).
  - Skills (bullets).

### 5. Cleaning and de-duplication
- **Boilerplate removed:** Standalone “Resume”, “:Resume:”, “CAREER OBJECTIVE”, “Personal details”, etc.
- **Replacement / bad characters:** Stripped so they don’t appear in the output.
- **Duplicate header fields removed:** Lines that are only Name :, Contact no :, Email id :, Date of birth :, DOB :, Address :, Gender : (or combinations) are dropped so they don’t repeat the top block.
- **Name + address line:** If a line is “&lt;Name at top&gt; At: …” it’s dropped (name already in header).
- **Career objective in body:** The same career objective text is removed from Experience & Background so it appears only under Career Objective.
- **Declaration and sign-off removed:** Any line containing “I hereby solemnly declare” or “above is true to the best of my knowledge”, and lines like “Your Faithfully”, “Yours Sincerely”, “Mr. &lt;NAME&gt;”, are stripped in the cleaner and skipped when writing; multi-line declaration/sign-off blocks are skipped entirely.

### 6. Experience & Background reorganization
- **Interested Field** – Shown as “Interested Field: &lt;value&gt;” (bold).
- **Company Name :- X - Location** – Shown as a bold company/location line.
- **Duty lines** – Lines starting with “I am”, “Performing”, “Operation”, “Operat”, “Fill the”, “CIP”, “SIP”, etc., or long lines with “operating”/“performing”/“manufacturing”/“batch” are rendered as bullets.
- **Experience intro** – Short lines with years/dates/“associate”/“technician”/“apprentice” as normal paragraphs.
- **Declaration/sign-off** – Not written; all related lines are skipped.

### 7. CLI
- `main.py` with `--input`, `--profile`, `--output-docx`, `--output-pdf` (optional).
- Uses profile JSON for all structured data; input PDF is used for extraction when run via CLI flow.

---

## Files

| File / folder        | Role |
|----------------------|------|
| `app.py`             | Streamlit app: upload, form, generate, download DOCX |
| `main.py`            | Extraction, parsing, cleaning, DOCX build, CLI |
| `profiles/example_profile.json` | Sample profile (name, contact, position, company, skills, experience, education) |
| `requirements.txt`   | Dependencies (e.g. pdfplumber, pytesseract, Pillow, python-docx, streamlit, docx2pdf) |
| `README.md`          | Setup, usage, project layout |
| `Current_Status.md`  | This file – current status and feature list |

---

## How to run

- **UI:**  
  `conda run -n torch_env streamlit run app.py`  
  Then open the URL (e.g. http://localhost:8501), upload a CV, pick up details, fill the form, and generate + download.

- **CLI:**  
  `conda run -n torch_env python main.py --input <path-to-cv> --profile profiles/example_profile.json --output-docx output/updated_cv.docx [--output-pdf]`

---

## Possible next steps (not yet done)

- PDF export in UI (e.g. “Download PDF” when Word/docx2pdf is available).
- Editable “Career Objective” in the form (pre-filled from parsing).
- More experience/education parsing rules for different CV formats.
- Optional “attach original extracted text at end” for debugging.
