def select_relevant_skills(profile_skills: list, jd_skills: list):
    relevant = []

    for skill in profile_skills:
        if skill.lower() in [jd.lower() for jd in jd_skills]:
            relevant.append(skill)

    return relevant