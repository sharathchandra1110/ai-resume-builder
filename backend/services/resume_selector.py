from backend.services.skill_extractor import dedupe_skills, normalize_skill_name


def select_relevant_skills(profile_skills: list, jd_skills: list):
    relevant = []
    jd_skill_keys = {normalize_skill_name(skill).lower() for skill in dedupe_skills(jd_skills)}

    for skill in dedupe_skills(profile_skills):
        normalized_skill = normalize_skill_name(skill)
        if normalized_skill.lower() in jd_skill_keys:
            relevant.append(normalized_skill)

    return relevant
