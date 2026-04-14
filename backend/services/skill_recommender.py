SKILL_LEARNING_MAP = {
    "Java": "Practice object-oriented programming, collections, and backend application development with Java.",
    "Spring Boot": "Learn Spring Boot fundamentals, build REST APIs, and practice with small backend projects.",
    "REST APIs": "Understand HTTP methods, status codes, and build CRUD APIs.",
    "MySQL": "Learn SQL queries, joins, indexing, and database design basics.",
    "PostgreSQL": "Practice schema design, joins, indexing, and writing efficient SQL queries in PostgreSQL.",
    "FastAPI": "Practice building APIs with FastAPI and integrating databases.",
    "React": "Learn component-based UI, hooks, and API integration.",
    "Git": "Build comfort with branching, commits, pull requests, and collaborative version control workflows.",
    "Docker": "Containerize a small app, learn Dockerfiles, and understand image and container basics.",
    "AWS": "Start with core AWS services like EC2, S3, and IAM while deploying simple applications.",
    "JWT": "Learn token-based authentication flows and implement secure login-protected APIs.",
    "Data Structures & Algorithms": "Practice arrays, linked lists, trees, hashing, and common interview-style problems.",
}

def recommend_skills(missing_skills: list):
    recommendations = {}

    for skill in missing_skills:
        recommendations[skill] = SKILL_LEARNING_MAP.get(
            skill,
            "Start with fundamentals and build small projects related to this skill."
        )

    return recommendations
