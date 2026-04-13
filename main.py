from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil, os, uuid

from src.parser    import extract_faces_with_thickness
from src.rules     import check_rules
from src.ai_engine import enrich_issues_with_ai, generate_summary
from src.report    import generate_pdf

app = FastAPI(title="DesignSense AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    # save uploaded file
    file_id   = str(uuid.uuid4())[:8]
    save_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # pipeline
    faces   = extract_faces_with_thickness(save_path)
    issues  = check_rules(faces)
    issues  = enrich_issues_with_ai(issues)
    summary = generate_summary(issues, file.filename)

    return {
        "filename":   file.filename,
        "face_count": len(faces),
        "issue_count": len(issues),
        "summary":    summary,
        "issues":     issues,
    }


@app.post("/report")
async def report(file: UploadFile = File(...)):
    # same pipeline but returns PDF
    file_id   = str(uuid.uuid4())[:8]
    save_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
    
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    faces   = extract_faces_with_thickness(save_path)
    issues  = check_rules(faces)
    issues  = enrich_issues_with_ai(issues)
    summary = generate_summary(issues, file.filename)

    pdf_path = generate_pdf(file.filename, summary, issues, file_id)
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"validation_{file_id}.pdf")


@app.get("/health")
def health():
    return {"status": "ok"}