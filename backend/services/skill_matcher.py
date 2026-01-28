def match_skills(profile_skills: list, jd_skills: list):
    profile_set = set(skill.lower() for skill in profile_skills)
    jd_set = set(skill.lower() for skill in jd_skills)

    matched = [skill for skill in jd_skills if skill.lower() in profile_set]
    missing = [skill for skill in jd_skills if skill.lower() not in profile_set]

    return {
        "matched_skills": matched,
        "missing_skills": missing
    }