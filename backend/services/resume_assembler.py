def assemble_resume(summary: str, skills_section: str):
    resume_text = f"""
{summary}

{skills_section}
"""
    return resume_text.strip()