from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil

from utils import extract_text_from_pdf, preprocess, semantic_similarity
from skills import extract_skills, missing_skills

app = FastAPI()

# ✅ CORS (VERY IMPORTANT for Netlify UI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your Netlify URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Basic Rate Limiting (simple version)
request_count = {}

@app.middleware("http")
async def rate_limit(request, call_next):
    ip = request.client.host
    request_count[ip] = request_count.get(ip, 0) + 1

    if request_count[ip] > 50:
        return {"error": "Too many requests"}

    response = await call_next(request)
    return response


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):

    file_path = file.filename

    with open(file_path, "wb") as buffer: # type: ignore
        shutil.copyfileobj(file.file, buffer)

    resume_text = extract_text_from_pdf(file_path)

    resume_clean = preprocess(resume_text)
    jd_clean = preprocess(job_desc)

    score = semantic_similarity(resume_clean, jd_clean)

    res_skills = extract_skills(resume_clean)
    jd_skills = extract_skills(jd_clean)

    missing = missing_skills(res_skills, jd_skills)

    return {
        "match_score": score,
        "resume_skills": res_skills,
        "jd_skills": jd_skills,
        "missing_skills": missing
    }