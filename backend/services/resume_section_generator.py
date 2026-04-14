from typing import Dict, List

from backend.services.skill_extractor import dedupe_skills


TECHNICAL_SKILL_GROUPS = {
    "Programming Languages": {"Java", "Python", "C", "C++", "JavaScript", "TypeScript", "HTML", "CSS"},
    "Backend & REST APIs": {"Spring Boot", "FastAPI", "REST APIs", "JWT"},
    "Databases": {"MySQL", "PostgreSQL"},
    "Tools & Environment": {"Git", "Docker", "AWS", "React"},
    "Data Structures & Algorithms": {"Data Structures & Algorithms", "OOP"},
}


def build_core_competencies(profile_skills: List[str], matched_skills: List[str]) -> List[str]:
    competencies = dedupe_skills(matched_skills + profile_skills)
    return competencies[:8]


def build_technical_skill_groups(skills: List[str]) -> Dict[str, List[str]]:
    normalized_skills = dedupe_skills(skills)
    categorized_skills: Dict[str, List[str]] = {}
    assigned = set()

    for group_name, group_skills in TECHNICAL_SKILL_GROUPS.items():
        items = [skill for skill in normalized_skills if skill in group_skills]
        if items:
            categorized_skills[group_name] = items
            assigned.update(items)

    remaining = [skill for skill in normalized_skills if skill not in assigned]
    if remaining:
        categorized_skills["Additional Skills"] = remaining

    return categorized_skills


def generate_skills_section(resume_skills: list):
    if not resume_skills:
        return "Technical Skills: Currently developing job-relevant technical skills."

    skills_text = ", ".join(dedupe_skills(resume_skills))
    return f"Technical Skills: {skills_text}"
