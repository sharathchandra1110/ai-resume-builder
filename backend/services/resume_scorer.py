def calculate_resume_score(matched_skills: list, jd_skills: list):
    if not jd_skills:
        return 0

    score = (len(matched_skills) / len(jd_skills)) * 100
    return round(score, 2)