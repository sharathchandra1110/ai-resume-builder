from fastapi import FastAPI

from backend.models.profile_models import UserProfile
from backend.models.jd_models import JobDescription

from backend.services.skill_extractor import extract_skills
from backend.services.skill_matcher import match_skills
from backend.services.resume_scorer import calculate_resume_score
from backend.services.skill_recommender import recommend_skills
from backend.services.resume_selector import select_relevant_skills
from backend.services.resume_summary_generator import generate_resume_summary
from backend.services.resume_section_generator import generate_skills_section
from backend.services.resume_assembler import assemble_resume
from backend.services.template_renderer import render_resume
from backend.services.template_registry import TEMPLATES
from backend.services.pdf_generator import generate_pdf_from_html
from fastapi.responses import FileResponse
import os

app = FastAPI()

# -------------------------
# In-memory storage
# -------------------------
stored_profile = None
stored_jd = None


# -------------------------
# Root
# -------------------------
@app.get("/")
def root():
    return {"message": "Backend is running successfully"}


# -------------------------
# Profile APIs
# -------------------------
@app.post("/profile")
def save_profile(profile: UserProfile):
    global stored_profile
    stored_profile = profile
    return {"message": "Profile saved successfully"}


@app.get("/profile")
def get_profile():
    if stored_profile is None:
        return {"message": "No profile found"}
    return stored_profile


# -------------------------
# Job Description APIs
# -------------------------
@app.post("/job-description")
def save_job_description(jd: JobDescription):
    global stored_jd
    stored_jd = jd.jd_text
    return {"message": "Job description saved successfully"}


@app.get("/job-description/skills")
def get_jd_skills():
    if stored_jd is None:
        return {"message": "No job description found"}

    skills = extract_skills(stored_jd)
    return {"extracted_skills": skills}


# -------------------------
# Skill Matching API
# -------------------------
@app.get("/skill-match")
def get_skill_match():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)

    return match_skills(profile_skills, jd_skills)
@app.get("/resume-score")
def get_resume_score():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    jd_skills = extract_skills(stored_jd)
    profile_skills = stored_profile.skills

    matched = match_skills(profile_skills, jd_skills)["matched_skills"]
    score = calculate_resume_score(matched, jd_skills)

    return {
        "resume_score": f"{score}%",
        "matched_skills": matched,
        "total_jd_skills": jd_skills
    }
@app.get("/skill-recommendations")
def get_skill_recommendations():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)

    match_result = match_skills(profile_skills, jd_skills)
    missing_skills = match_result["missing_skills"]

    recommendations = recommend_skills(missing_skills)

    return {
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }
@app.get("/resume/skills")
def get_resume_skills():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)

    resume_skills = select_relevant_skills(profile_skills, jd_skills)

    return {
        "resume_skills": resume_skills
    }
@app.get("/resume/summary")
def get_resume_summary():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    name = stored_profile.name
    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)

    resume_skills = select_relevant_skills(profile_skills, jd_skills)
    summary = generate_resume_summary(name, resume_skills, stored_jd)

    return {
        "resume_summary": summary
    }
@app.get("/resume/skills-section")
def get_resume_skills_section():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)

    resume_skills = select_relevant_skills(profile_skills, jd_skills)
    skills_section = generate_skills_section(resume_skills)

    return {
        "skills_section": skills_section
    }
@app.get("/resume/full")
def get_full_resume():
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    name = stored_profile.name
    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)

    resume_skills = select_relevant_skills(profile_skills, jd_skills)
    summary = generate_resume_summary(name, resume_skills, stored_jd)
    skills_section = generate_skills_section(resume_skills)

    full_resume = assemble_resume(summary, skills_section)

    return {
        "full_resume": full_resume
    }
@app.get("/templates")
def list_resume_templates():
    return {
        "available_templates": TEMPLATES
    }
@app.get("/resume/html")
def generate_html_resume(template_id: str = "ats_single_column"):
    if stored_profile is None:
        return {"message": "No profile found"}

    if stored_jd is None:
        return {"message": "No job description found"}

    # Build resume content (reuse existing logic)
    name = stored_profile.name
    email = stored_profile.email
    phone = getattr(stored_profile, "phone", "")
    location = getattr(stored_profile, "location", "")

    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)
    resume_skills = select_relevant_skills(profile_skills, jd_skills)

    summary = generate_resume_summary(name, resume_skills, stored_jd)
    skills_text = ", ".join(resume_skills)
    education = stored_profile.education

    # Simple experience placeholder (we’ll improve later)
    experience_items = "<li>Relevant academic and project experience</li>"

    context = {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "summary": summary,
        "skills": skills_text,
        "education": education,
        "experience": experience_items
    }

    html = render_resume(f"{template_id}.html", context)

    return {
        "html_resume": html
    }
@app.get("/resume/pdf")
def generate_pdf_resume(template_id: str = "ats_single_column"):
    if stored_profile is None or stored_jd is None:
        return {"message": "Profile or Job Description missing"}

    name = stored_profile.name
    email = stored_profile.email
    phone = getattr(stored_profile, "phone", "")
    location = getattr(stored_profile, "location", "")
    education = stored_profile.education

    profile_skills = stored_profile.skills
    jd_skills = extract_skills(stored_jd)
    resume_skills = select_relevant_skills(profile_skills, jd_skills)

    summary = generate_resume_summary(name, resume_skills, stored_jd)
    skills_text = ", ".join(resume_skills)

    experience_items = "<li>Relevant academic and project experience</li>"

    context = {
        "name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "summary": summary,
        "skills": skills_text,
        "education": education,
        "experience": experience_items
    }

    html = render_resume(f"{template_id}.html", context)

    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = f"{output_dir}/{name.replace(' ', '_')}_resume.pdf"

    generate_pdf_from_html(html, pdf_path)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )