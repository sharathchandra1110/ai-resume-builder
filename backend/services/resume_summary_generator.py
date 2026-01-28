def generate_resume_summary(name: str, resume_skills: list, jd_text: str):
    if not resume_skills:
        return f"{name} is a motivated candidate actively building skills aligned with the job requirements."

    skills_text = ", ".join(resume_skills)

    summary = (
        f"{name} is a motivated software professional with hands-on experience in "
        f"{skills_text}. Passionate about building scalable applications and aligning "
        f"technical skills with industry requirements."
    )

    return summary