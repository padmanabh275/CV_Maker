import io
import json
import re
from typing import Any, Dict

import pdfplumber
import pytesseract
import streamlit as st
from docx import Document
from PIL import Image

from main import build_cv_doc, parse_cv_into_structured_fields


def extract_text_from_upload(uploaded_file) -> str:
    """Extract text from uploaded PDF or image using pdfplumber / pytesseract."""
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.type or ""
    try:
        if file_type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                pages_text = [(page.extract_text() or "") for page in pdf.pages]
            return "\n".join(pages_text)
        else:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
            return text or ""
    except Exception as e:
        # In UI we will show a generic warning; detailed error is printed to console
        print(f"Error extracting text from upload: {e}")
        return ""


def parse_cv_text(text: str) -> Dict[str, Any]:
    """Very simple heuristics to guess name, email, phone, and skills from CV text."""
    result: Dict[str, Any] = {}
    if not text:
        return result

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    # Name: first non-empty line
    if lines:
        result["name"] = lines[0]

    # Email
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if email_match:
        result["email"] = email_match.group(0)

    # Phone (very loose pattern for mobile numbers)
    phone_match = re.search(r"(\+?\d[\d\s\-]{8,}\d)", text)
    if phone_match:
        result["phone"] = phone_match.group(0).strip()

    # Try to detect a simple "Skills" section and turn into a list
    skills_idx = None
    for i, line in enumerate(lines):
        if re.search(r"\bskills\b", line, re.IGNORECASE):
            skills_idx = i
            break

    if skills_idx is not None:
        skills_lines = []
        for l in lines[skills_idx + 1 :]:
            # Stop if blank or looks like a new uppercase heading
            if not l.strip():
                break
            if re.match(r"^[A-Z][A-Z\s]{2,}$", l):
                break
            skills_lines.append(l)

        if skills_lines:
            skills_text = " ".join(skills_lines)
            raw_skills = re.split(r"[,\u2022•;|-]+", skills_text)
            skills = [s.strip() for s in raw_skills if s.strip()]
            if skills:
                result["skills"] = skills

    return result


def create_profile_from_inputs(
    base_profile: Dict[str, Any],
    name: str,
    email: str,
    location: str,
    position: str,
    phone: str,
    original_text: str,
) -> Dict[str, Any]:
    """Merge extracted data and user answers into a profile dict used to build the CV."""
    profile = dict(base_profile) if base_profile else {}

    # Basic safe defaults
    profile.setdefault("name", "Candidate Name")
    profile.setdefault("email", "")
    profile.setdefault("location", "")
    profile.setdefault("summary", "")
    profile.setdefault("skills", [])
    profile.setdefault("experience", [])

    if name:
        profile["name"] = name
    if email:
        profile["email"] = email
    if location:
        profile["location"] = location
    if phone:
        profile["phone"] = phone
    if position:
        profile["current_position"] = position
    if original_text:
        profile["original_text"] = original_text

    return profile


def document_to_bytes(doc: Document) -> bytes:
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()


def main() -> None:
    st.set_page_config(page_title="CV Updater", page_icon="📄", layout="centered")
    st.title("CV Updater")
    st.write(
        "Upload a CV (PDF or image). The app will try to read basic details, then ask you a few "
        "questions (position, phone, etc.) before generating a new CV."
    )

    if "auto_profile" not in st.session_state:
        st.session_state["auto_profile"] = {}

    uploaded_file = st.file_uploader("Upload CV (PDF or image)", type=["pdf", "png", "jpg", "jpeg"])

    raw_text = ""
    if uploaded_file is not None:
        if st.button("Pick up details from this CV"):
            raw_text = extract_text_from_upload(uploaded_file)
            if not raw_text:
                st.warning("Could not extract text from the uploaded CV. You can still fill details manually.")
            else:
                auto_data = parse_cv_text(raw_text)
                st.session_state["auto_profile"] = auto_data
                st.session_state["raw_text"] = raw_text
                st.success("Picked up details from CV. You can review and edit them below.")
        else:
            # If user already picked up details in this session, reuse stored text
            raw_text = st.session_state.get("raw_text", "")

    auto_profile: Dict[str, Any] = st.session_state.get("auto_profile", {})

    if raw_text:
        st.markdown("### Extracted CV text")
        st.text_area("Extracted text (read-only)", value=raw_text, height=200)

    st.markdown("### Basic details")
    name = st.text_input("Name", value=auto_profile.get("name", ""))
    email = st.text_input("Email", value=auto_profile.get("email", ""))
    location = st.text_input("Location (optional)", value=auto_profile.get("location", ""))

    st.markdown("### Position")
    position_options = [
        "Software Engineer",
        "Senior Software Engineer",
        "Team Lead",
        "Data Scientist",
        "Senior Data Scientist",
        "Product Manager",
        "Custom...",
    ]
    selected_position = st.selectbox("Select position", position_options, index=0)
    custom_position = ""
    if selected_position == "Custom...":
        custom_position = st.text_input("Enter custom position")

    st.markdown("### Current company")
    current_company = st.text_input("Enter current company (optional)", value=auto_profile.get("current_company", ""))

    st.markdown("### Current position")
    current_position = st.text_input("Enter current position (optional)", value=auto_profile.get("current_position", ""))

    st.markdown("### Phone number")
    phone = st.text_input("Enter phone number", value=auto_profile.get("phone", ""))

    generate_btn = st.button("Generate New CV")

    if generate_btn:
        if uploaded_file is None:
            st.error("Please upload a CV file first.")
            return

        # Ensure we have full CV text for the document (extract now if not already done)
        text_for_doc = raw_text or extract_text_from_upload(uploaded_file)

        # Parse structured fields (Name, DOB, Career Objective, Experience) from extracted text
        structured = parse_cv_into_structured_fields(text_for_doc)
        if structured.get("name") and not name:
            name = structured["name"]

        if not phone:
            st.error("Please enter a phone number.")
            return

        # Determine final position value
        if selected_position == "Custom...":
            position_value = custom_position.strip()
        else:
            position_value = selected_position

        if not position_value:
            st.error("Please select or enter a position.")
            return

        profile = create_profile_from_inputs(
            base_profile=auto_profile,
            name=name,
            email=email,
            location=location,
            position=position_value,
            phone=phone,
            original_text=text_for_doc,
        )
        if current_company:
            profile["current_company"] = current_company
        if current_position:
            profile["current_position"] = current_position
        if structured.get("dob"):
            profile["dob"] = structured["dob"]
        if structured.get("career_objective"):
            profile["career_objective"] = structured["career_objective"]
        if structured.get("experience"):
            profile["experience"] = structured["experience"]

        # Build the document using existing helper
        doc = build_cv_doc(profile)
        doc_bytes = document_to_bytes(doc)

        st.success("New CV generated successfully.")
        st.download_button(
            label="Download DOCX",
            data=doc_bytes,
            file_name="updated_cv.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )


if __name__ == "__main__":
    main()

