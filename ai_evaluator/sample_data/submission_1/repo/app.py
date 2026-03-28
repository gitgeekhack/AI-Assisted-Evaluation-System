from fastapi import FastAPI

app = FastAPI()

def extract_skills(text):
    return ["Python", "ML"]

def score_candidate(skills):
    return len(skills) * 10

@app.post("/analyze")
def analyze_resume(text: str):
    skills = extract_skills(text)
    score = score_candidate(skills)
    return {"skills": skills, "score": score}