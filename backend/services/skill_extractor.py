SKILL_KEYWORDS = [
    "Python",
    "Java",
    "C",
    "Spring Boot",
    "FastAPI",
    "REST",
    "REST APIs",
    "MySQL",
    "PostgreSQL",
    "React",
    "JavaScript",
    "HTML",
    "CSS"
]

def extract_skills(jd_text: str):
    found_skills = []

    for skill in SKILL_KEYWORDS:
        if skill.lower() in jd_text.lower():
            found_skills.append(skill)

    return list(set(found_skills))