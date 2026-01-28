SKILL_LEARNING_MAP = {
    "Spring Boot": "Learn Spring Boot fundamentals, build REST APIs, and practice with small backend projects.",
    "REST APIs": "Understand HTTP methods, status codes, and build CRUD APIs.",
    "MySQL": "Learn SQL queries, joins, indexing, and database design basics.",
    "FastAPI": "Practice building APIs with FastAPI and integrating databases.",
    "React": "Learn component-based UI, hooks, and API integration."
}

def recommend_skills(missing_skills: list):
    recommendations = {}

    for skill in missing_skills:
        recommendations[skill] = SKILL_LEARNING_MAP.get(
            skill,
            "Start with fundamentals and build small projects related to this skill."
        )

    return recommendations