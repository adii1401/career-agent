import os
from dotenv import load_dotenv
from resume_store import load_resume, resume_exists
from agents.company_researcher import research_company
from agents.jd_analyzer import analyze_jd
from agents.gap_analyzer import analyze_gap
from agents.resume_tailor import tailor_resume
from agents.interview_prep import generate_interview_prep

load_dotenv()

def extract_company_name(jd_text: str) -> str:
    lines = jd_text.strip().split("\n")
    for line in lines[:5]:
        if line.strip():
            return line.strip()[:50]
    return "the company"

def run_career_agent(jd_text: str, resume_text: str = None) -> dict:
    if not resume_text:
        resume_text = load_resume()
    if not resume_text:
        return {"error": "No resume found. Please upload your resume first."}

    results = {}

    print("Step 1/5: Researching company...")
    company_name = extract_company_name(jd_text)
    results["company_research"] = research_company(company_name)

    print("Step 2/5: Analyzing job description...")
    results["jd_analysis"] = analyze_jd(jd_text)

    print("Step 3/5: Analyzing gaps...")
    results["gap_analysis"] = analyze_gap(resume_text, results["jd_analysis"])

    print("Step 4/5: Tailoring resume...")
    results["tailored_resume"] = tailor_resume(resume_text, jd_text, results["jd_analysis"])

    print("Step 5/5: Generating interview prep...")
    results["interview_prep"] = generate_interview_prep(
        resume_text, jd_text, results["company_research"]
    )

    print("Done!")
    return results

if __name__ == "__main__":
    sample_jd = """
    TechCorp AI — AI Automation Engineer
    Build LLM-powered applications using Python, FastAPI, LangChain.
    Deploy on cloud platforms. Work with RAG pipelines and vector databases.
    2-5 years experience required.
    """

    # Save a test resume first
    from resume_store import save_resume
    save_resume("""
    Aditya Kumar Gupta — AI Automation Engineer
    3+ years at Cognizant in MFT/EDI and B2B integration.
    AI Projects: MFT Operations Agent (LangGraph, FastAPI, ChromaDB, Docker)
    MFT Email Responder (RAG, ChromaDB, Microsoft Graph API)
    Skills: Python, LangGraph, FastAPI, ChromaDB, RAG, Docker, Git
    """)

    results = run_career_agent(sample_jd)
    for key, value in results.items():
        print(f"\n{'='*50}")
        print(f"{key.upper()}")
        print('='*50)
        print(value)