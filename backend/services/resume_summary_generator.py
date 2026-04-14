def generate_resume_summary(name: str, resume_skills: list, jd_text: str, headline: str = ""):
    role = headline.strip() or "software developer"

    if not resume_skills:
        return (
            f"{name} is a motivated {role.lower()} with a strong foundation in problem solving, "
            f"software development, and learning technologies aligned with the target role."
        )

    top_skills = ", ".join(resume_skills[:4])
    if len(resume_skills) > 4:
        top_skills = f"{top_skills}, and {len(resume_skills) - 4} more"

    return (
        f"{name} is a detail-oriented {role.lower()} with hands-on experience in {top_skills}. "
        f"Focused on building reliable applications, writing clean backend logic, and matching "
        f"technical strengths to job requirements."
    )
