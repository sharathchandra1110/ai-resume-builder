from backend.services.skill_extractor import dedupe_skills, normalize_skill_name


def match_skills(profile_skills: list, jd_skills: list):
    normalized_profile = {
        normalize_skill_name(skill).lower(): normalize_skill_name(skill)
        for skill in dedupe_skills(profile_skills)
    }

    matched = []
    missing = []

    for skill in dedupe_skills(jd_skills):
        normalized_skill = normalize_skill_name(skill)
        if normalized_skill.lower() in normalized_profile:
            matched.append(normalized_skill)
        else:
            missing.append(normalized_skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
    }
