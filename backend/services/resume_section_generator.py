def generate_skills_section(resume_skills: list):
    if not resume_skills:
        return "Skills: Currently developing job-relevant technical skills."

    skills_text = ", ".join(resume_skills)
    return f"Skills: {skills_text}"