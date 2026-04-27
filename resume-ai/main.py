from utils import extract_text_from_pdf, preprocess, semantic_similarity
from skills import extract_skills, missing_skills

# Load resume
resume_text = extract_text_from_pdf("sample_resume.pdf")

# Example Job Description
job_desc = """
Looking for .NET developer with experience in ASP.NET Core, SQL Server, Azure, Microservices
"""

# Process text
resume_clean = preprocess(resume_text)
jd_clean = preprocess(job_desc)

# Similarity score
score = semantic_similarity(resume_clean, jd_clean)

# Skill analysis
resume_skills = extract_skills(resume_clean)
jd_skills = extract_skills(jd_clean)

missing = missing_skills(resume_skills, jd_skills)

# Output
print("\n--- RESULT ---")
print("Match Score:", score, "%")
print("Resume Skills:", resume_skills)
print("JD Skills:", jd_skills)
print("Missing Skills:", missing)