import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
from dotenv import load_dotenv

load_dotenv()

from resume_store import process_resume_file, load_resume, resume_exists, save_resume
from main import run_career_agent

app = FastAPI(title="CareerAgent")
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    jd_text: str
    resume_text: str = None

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        ext = file.filename.split(".")[-1].lower()
        if ext not in ["pdf", "docx", "doc", "txt"]:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")
        
        temp_path = f"./temp_resume.{ext}"
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        text = process_resume_file(temp_path)
        os.remove(temp_path)
        
        return {"status": "success", "message": "Resume uploaded successfully.", "preview": text[:300]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/resume-status")
async def resume_status():
    if resume_exists():
        text = load_resume()
        return {"exists": True, "preview": text[:300]}
    return {"exists": False}

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        if not request.jd_text.strip():
            raise HTTPException(status_code=400, detail="Job description is required.")
        results = run_career_agent(request.jd_text, request.resume_text)
        if "error" in results:
            raise HTTPException(status_code=400, detail=results["error"])
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)