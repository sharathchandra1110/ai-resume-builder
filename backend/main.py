import re
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from backend.models.jd_models import JobDescription
from backend.models.profile_models import ResumeItem, UserProfile
from backend.services.pdf_generator import generate_pdf_from_html
from backend.services.resume_assembler import assemble_resume
from backend.services.resume_scorer import calculate_resume_score
from backend.services.resume_section_generator import (
    build_core_competencies,
    build_technical_skill_groups,
    generate_skills_section,
)
from backend.services.resume_selector import select_relevant_skills
from backend.services.resume_summary_generator import generate_resume_summary
from backend.services.skill_extractor import dedupe_skills, extract_skills
from backend.services.skill_matcher import match_skills
from backend.services.skill_recommender import recommend_skills
from backend.services.state_store import AppStateStore
from backend.services.template_registry import TEMPLATES, get_template
from backend.services.template_renderer import render_resume


app = FastAPI(
    title="Resume AI Builder API",
    version="2.0.0",
    description="Generate job-targeted resumes in a sample-inspired professional format.",
)

state_store = AppStateStore()
PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"
FRONTEND_DIR = PROJECT_ROOT / "frontend"


def _model_dump(model: Any) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "resume"


def _require_profile() -> UserProfile:
    profile = state_store.get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail="No profile found. Save a profile first.")
    return profile


def _require_job_description() -> JobDescription:
    job_description = state_store.get_job_description()
    if not job_description:
        raise HTTPException(status_code=404, detail="No job description found. Save one first.")
    return job_description


def _require_template(template_id: str) -> Dict[str, str]:
    template = get_template(template_id)
    if template is None:
        available = ", ".join(item["id"] for item in TEMPLATES)
        raise HTTPException(
            status_code=404,
            detail=f"Template '{template_id}' was not found. Available templates: {available}",
        )
    return template


def _serialize_resume_item(item: ResumeItem) -> Dict[str, Any]:
    data = _model_dump(item)
    data["technologies"] = dedupe_skills(data.get("technologies", []))
    data["highlights"] = [highlight.strip() for highlight in data.get("highlights", []) if highlight.strip()]
    return data


def _build_resume_analysis(profile: UserProfile, jd_text: str) -> Dict[str, Any]:
    jd_skills = extract_skills(jd_text)
    match_result = match_skills(profile.skills, jd_skills)
    matched_skills = match_result["matched_skills"]
    missing_skills = match_result["missing_skills"]
    selected_skills = select_relevant_skills(profile.skills, jd_skills)
    fallback_skills = dedupe_skills(profile.core_competencies + profile.skills)
    resume_skills = selected_skills or fallback_skills

    return {
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_score": calculate_resume_score(matched_skills, jd_skills),
        "resume_skills": resume_skills,
        "summary": generate_resume_summary(
            profile.name,
            resume_skills,
            jd_text,
            headline=profile.headline,
        ),
        "core_competencies": build_core_competencies(
            profile.core_competencies or profile.skills,
            matched_skills,
        ),
        "technical_skills": build_technical_skill_groups(profile.skills),
        "recommendations": recommend_skills(missing_skills),
    }


def _build_resume_context(profile: UserProfile, jd_text: str) -> Dict[str, Any]:
    analysis = _build_resume_analysis(profile, jd_text)
    links = [{"label": label, "url": url} for label, url in profile.links.items() if url.strip()]
    contact_parts = [part for part in [profile.phone, profile.email, profile.location] if part.strip()]
    contact_parts.extend(link["label"] for link in links)

    return {
        "name": profile.name,
        "headline": profile.headline or "Backend Developer",
        "email": profile.email,
        "phone": profile.phone,
        "location": profile.location,
        "contact_parts": contact_parts,
        "links": links,
        "summary": analysis["summary"],
        "core_competencies": analysis["core_competencies"],
        "technical_skills": analysis["technical_skills"],
        "skills_text": ", ".join(analysis["resume_skills"]),
        "education": profile.education,
        "experience": [_serialize_resume_item(item) for item in profile.experience],
        "projects": [_serialize_resume_item(item) for item in profile.projects],
        "certifications": [cert for cert in profile.certifications if cert.strip()],
        "resume_score": analysis["resume_score"],
        "missing_skills": analysis["missing_skills"],
    }


@app.get("/")
def root():
    return {
        "message": "Resume AI Builder backend is running",
        "default_template": "ats_single_column",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "storage": state_store.snapshot(),
        "available_templates": [template["id"] for template in TEMPLATES],
    }


@app.post("/profile")
def save_profile(profile: UserProfile):
    state_store.save_profile(profile)
    return {
        "message": "Profile saved successfully",
        "profile_strength": {
            "skills_count": len(dedupe_skills(profile.skills)),
            "projects_count": len(profile.projects),
            "experience_count": len(profile.experience),
        },
    }


@app.get("/profile")
def get_profile():
    return _require_profile()


@app.post("/job-description")
def save_job_description(jd: JobDescription):
    state_store.save_job_description(jd)
    return {
        "message": "Job description saved successfully",
        "extracted_skills": extract_skills(jd.jd_text),
        "target_title": jd.target_title,
        "company_name": jd.company_name,
    }


@app.get("/job-description")
def get_job_description():
    return _require_job_description()


@app.get("/job-description/skills")
def get_jd_skills():
    job_description = _require_job_description()
    return {"extracted_skills": extract_skills(job_description.jd_text)}


@app.delete("/state/reset")
def reset_state():
    state_store.clear()
    return {"message": "Stored profile and job description cleared successfully"}


@app.get("/skill-match")
def get_skill_match():
    profile = _require_profile()
    job_description = _require_job_description()
    jd_skills = extract_skills(job_description.jd_text)
    return match_skills(profile.skills, jd_skills)


@app.get("/resume-score")
def get_resume_score():
    profile = _require_profile()
    job_description = _require_job_description()
    analysis = _build_resume_analysis(profile, job_description.jd_text)

    return {
        "resume_score": f"{analysis['resume_score']}%",
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"],
        "total_jd_skills": analysis["jd_skills"],
    }


@app.get("/skill-recommendations")
def get_skill_recommendations():
    profile = _require_profile()
    job_description = _require_job_description()
    analysis = _build_resume_analysis(profile, job_description.jd_text)

    return {
        "missing_skills": analysis["missing_skills"],
        "recommendations": analysis["recommendations"],
    }


@app.get("/analysis/fit")
def get_fit_analysis():
    profile = _require_profile()
    job_description = _require_job_description()
    analysis = _build_resume_analysis(profile, job_description.jd_text)

    return {
        "resume_score": analysis["resume_score"],
        "matched_skills": analysis["matched_skills"],
        "missing_skills": analysis["missing_skills"],
        "core_competencies": analysis["core_competencies"],
        "recommendations": analysis["recommendations"],
    }


@app.get("/resume/skills")
def get_resume_skills():
    profile = _require_profile()
    job_description = _require_job_description()
    analysis = _build_resume_analysis(profile, job_description.jd_text)
    return {"resume_skills": analysis["resume_skills"]}


@app.get("/resume/summary")
def get_resume_summary_endpoint():
    profile = _require_profile()
    job_description = _require_job_description()
    analysis = _build_resume_analysis(profile, job_description.jd_text)
    return {"resume_summary": analysis["summary"]}


@app.get("/resume/skills-section")
def get_resume_skills_section():
    profile = _require_profile()
    job_description = _require_job_description()
    analysis = _build_resume_analysis(profile, job_description.jd_text)
    return {"skills_section": generate_skills_section(analysis["resume_skills"])}


@app.get("/resume/preview")
def get_resume_preview(template_id: str = "ats_single_column"):
    _require_template(template_id)
    profile = _require_profile()
    job_description = _require_job_description()
    context = _build_resume_context(profile, job_description.jd_text)

    return {
        "template_id": template_id,
        "header": {
            "name": context["name"],
            "headline": context["headline"],
            "email": context["email"],
            "phone": context["phone"],
            "location": context["location"],
            "links": context["links"],
        },
        "professional_summary": context["summary"],
        "core_competencies": context["core_competencies"],
        "technical_skills": context["technical_skills"],
        "projects": context["projects"],
        "experience": context["experience"],
        "education": context["education"],
        "certifications": context["certifications"],
        "resume_score": context["resume_score"],
    }


@app.get("/resume/full")
def get_full_resume():
    profile = _require_profile()
    job_description = _require_job_description()
    context = _build_resume_context(profile, job_description.jd_text)

    full_resume = assemble_resume(
        name=context["name"],
        headline=context["headline"],
        summary=context["summary"],
        core_competencies=context["core_competencies"],
        technical_skills=context["technical_skills"],
        education=context["education"],
        projects=context["projects"],
        experience=context["experience"],
    )

    return {"full_resume": full_resume}


@app.get("/templates")
def list_resume_templates():
    return {
        "default_template": "ats_single_column",
        "available_templates": TEMPLATES,
    }


@app.get("/resume/html")
def generate_html_resume(template_id: str = "ats_single_column"):
    template = _require_template(template_id)
    profile = _require_profile()
    job_description = _require_job_description()

    context = _build_resume_context(profile, job_description.jd_text)
    html = render_resume(template["file_name"], context)

    return {
        "template_id": template_id,
        "html_resume": html,
    }


@app.get("/resume/view", response_class=HTMLResponse)
def view_html_resume(template_id: str = "ats_single_column"):
    template = _require_template(template_id)
    profile = _require_profile()
    job_description = _require_job_description()

    context = _build_resume_context(profile, job_description.jd_text)
    html = render_resume(template["file_name"], context)
    return HTMLResponse(content=html)


@app.get("/resume/pdf")
def generate_pdf_resume(template_id: str = "ats_single_column"):
    template = _require_template(template_id)
    profile = _require_profile()
    job_description = _require_job_description()

    context = _build_resume_context(profile, job_description.jd_text)
    html = render_resume(template["file_name"], context)

    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = GENERATED_DIR / f"{_slugify(profile.name)}_resume.pdf"

    try:
        generate_pdf_from_html(html, str(pdf_path))
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return FileResponse(
        str(pdf_path),
        media_type="application/pdf",
        filename=pdf_path.name,
    )


@app.get("/app", include_in_schema=False)
def frontend_entry():
    return RedirectResponse(url="/app/")


app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
