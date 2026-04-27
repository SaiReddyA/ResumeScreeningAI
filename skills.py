SKILLS = [
    "python", "c#", ".net", "asp.net", "sql", "azure",
    "aws", "docker", "kubernetes", "react", "angular",
    "microservices", "api", "machine learning"
]


def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return found


def missing_skills(resume_skills, jd_skills):
    return list(set(jd_skills) - set(resume_skills))