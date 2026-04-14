import re
from typing import Dict, List


SKILL_PATTERNS: Dict[str, List[str]] = {
    "Java": [r"\bjava\b"],
    "Python": [r"\bpython\b"],
    "C++": [r"\bc\+\+\b"],
    "C": [r"(?<![A-Za-z0-9+])c(?![A-Za-z0-9+#])", r"\bc language\b", r"\bc programming\b"],
    "Spring Boot": [r"\bspring\s*boot\b"],
    "FastAPI": [r"\bfastapi\b"],
    "REST APIs": [r"\brest(?:ful)?\s+apis?\b", r"\brest(?:ful)?\b"],
    "MySQL": [r"\bmysql\b"],
    "PostgreSQL": [r"\bpostgres(?:ql)?\b"],
    "React": [r"\breact(?:\.js)?\b"],
    "JavaScript": [r"\bjavascript\b"],
    "TypeScript": [r"\btypescript\b"],
    "HTML": [r"\bhtml\b"],
    "CSS": [r"\bcss\b"],
    "Docker": [r"\bdocker\b"],
    "Git": [r"\bgit\b", r"\bgithub\b"],
    "AWS": [r"\baws\b", r"\bamazon web services\b"],
    "JWT": [r"\bjwt\b", r"\bjson web token\b"],
    "OOP": [r"\boop\b", r"\bobject oriented programming\b"],
    "Data Structures & Algorithms": [r"\bdata structures?\b", r"\balgorithms?\b", r"\bdsa\b"],
}

SKILL_ALIASES = {
    "rest": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "restful": "REST APIs",
    "restful api": "REST APIs",
    "restful apis": "REST APIs",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "github": "Git",
    "git": "Git",
    "object oriented programming": "OOP",
    "dsa": "Data Structures & Algorithms",
}

for skill_name in SKILL_PATTERNS:
    SKILL_ALIASES.setdefault(skill_name.lower(), skill_name)


def normalize_skill_name(skill: str) -> str:
    cleaned = " ".join(skill.strip().split())
    if not cleaned:
        return ""
    return SKILL_ALIASES.get(cleaned.lower(), cleaned)


def dedupe_skills(skills: List[str]) -> List[str]:
    unique_skills: List[str] = []
    seen = set()

    for skill in skills:
        normalized = normalize_skill_name(skill)
        if not normalized:
            continue

        key = normalized.lower()
        if key in seen:
            continue

        seen.add(key)
        unique_skills.append(normalized)

    return unique_skills


def extract_skills(jd_text: str) -> List[str]:
    text = jd_text or ""
    found_skills: List[str] = []

    for skill_name, patterns in SKILL_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            found_skills.append(skill_name)

    return dedupe_skills(found_skills)
